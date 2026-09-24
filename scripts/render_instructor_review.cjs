/* Print the prepared lecturer HTML using Chromium and local MathJax.
 * Set NODE_PATH to the directory containing playwright; BROWSER_EXECUTABLE
 * may select an installed Chromium/Edge. No existing browser session is used.
 */
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '..');
const work = path.join(root, 'tmp/pdfs/instructor_review');
const out = path.join(root, 'output/pdf/instructor_review');

(async () => {
  const browser = await chromium.launch({headless:true,
    ...(process.env.BROWSER_EXECUTABLE ? {executablePath:process.env.BROWSER_EXECUTABLE} : {})});
  try {
    const page = await browser.newPage({viewport:{width:1000,height:900}, deviceScaleFactor:2});
    await page.goto(pathToFileURL(path.join(out, '01_carbonate_explorer.html')).href);
    await page.waitForFunction(() => document.querySelector('#readout').textContent.length > 10);
    for (const mode of ['oblique','top','slice']) {
      await page.evaluate(mode => {
        document.querySelector('#'+mode).click();
        if (mode === 'slice') {
          for (const id of ['tangent','atmosphere']) {
            const input = document.querySelector('#'+id);
            if (!input.checked) input.click();
          }
        }
        document.querySelector('#download').style.display = 'none';
      }, mode);
      await page.locator('body').screenshot({path:path.join(work, `explorer-${mode}.png`)});
    }
    const report = [];
    for (const name of fs.readdirSync(work).filter(n => /^0[0-4]_.*\.html$/.test(n)).sort()) {
      const errors=[];
      const handler = e => errors.push(e.message);
      page.on('pageerror', handler);
      await page.setViewportSize({width:695,height:1000});
      await page.goto(pathToFileURL(path.join(work, name)).href, {waitUntil:'load'});
      await page.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise);
      await page.evaluate(() => MathJax.startup.promise);
      await page.evaluate(() => document.fonts.ready);
      await page.emulateMedia({media:'print'});
      const qa = await page.evaluate(() => {
        const images=[...document.images];
        const mathErrors=[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(e=>e.textContent);
        const closed=[...document.querySelectorAll('details:not([open])')].length;
        // Keep short questions/answers and compact reference tables together.
        // Long panels remain splittable so no content can overflow a page.
        for (const element of document.querySelectorAll("div[style*='background-color'], details, table")) {
          if (element.getBoundingClientRect().height < 610) element.style.breakInside='avoid';
        }
        // Fit wide mathematical displays to the page without rasterizing them.
        for (const container of document.querySelectorAll('mjx-container')) {
          const svg=container.querySelector('svg');
          if (svg && svg.getBoundingClientRect().width > container.parentElement.clientWidth) {
            container.style.fontSize = (container.parentElement.clientWidth/svg.getBoundingClientRect().width*98)+'%';
          }
        }
        const overflow=[...document.querySelectorAll('table,pre,img,mjx-container')]
          .filter(e=>e.getBoundingClientRect().right > document.body.clientWidth+2)
          .map(e=>({tag:e.tagName,text:e.textContent.slice(0,80),right:e.getBoundingClientRect().right}));
        return {math:document.querySelectorAll('mjx-container').length,mathErrors,closed,
          brokenImages:images.filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src.slice(0,100)),overflow};
      });
      if (errors.length || qa.mathErrors.length || qa.closed || qa.brokenImages.length) {
        throw Error(JSON.stringify({name,errors,...qa}));
      }
      const short=name.slice(0,2);
      await page.pdf({path:path.join(out,name.replace(/html$/, 'pdf')),format:'A4',
        printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,outline:true,tagged:true,
        headerTemplate:'<span></span>',
        footerTemplate:`<div style="font:8px Arial;color:#687585;width:100%;margin:0 13mm;display:flex;justify-content:space-between"><span>ESBMTK practical ${short} | Instructor review | 24 September 2026</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`});
      report.push({name,errors,...qa});
      console.log(JSON.stringify(report[report.length-1]));
      page.off('pageerror',handler);
    }
    fs.writeFileSync(path.join(work,'render-qa.json'),JSON.stringify(report,null,2));
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});
