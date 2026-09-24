// Optional authoring dependency: @oai/artifact-tool; not needed by students.
// Usage: node build_flux_worksheets.mjs records.json output-directory preview-directory
import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const [recordsPath, outputDir, previewDir] = process.argv.slice(2);
if (!recordsPath || !outputDir || !previewDir) throw new Error('Expected JSON, output and preview paths');
const records = JSON.parse(await fs.readFile(recordsPath, 'utf8'));
await fs.mkdir(outputDir, {recursive: true});
await fs.mkdir(previewDir, {recursive: true});
for (const role of ['student', 'instructor']) {
  const wb = Workbook.create();
  for (const [sheetName, rows] of Object.entries(records[role])) {
    const sh = wb.worksheets.add(sheetName);
    sh.showGridLines = false;
    sh.tabColor = role === 'student' ? '#3977B8' : '#7952A8';
    const headers = Object.keys(rows[0]);
    const lastCol = String.fromCharCode(65 + headers.length);
    const end = 6 + rows.length;
    const full = sh.getRange(`B2:${lastCol}${end}`);
    full.format.font = {name: 'Arial', size: 11, color: '#173B61'};
    full.format.verticalAlignment = 'center';
    full.format.wrapText = true;
    sh.getRange('A1:A20').format.columnWidthPx = 24;
    sh.getRange('B2').values = [[`${role === 'student' ? 'Student' : 'Instructor'} flux specification`]];
    sh.getRange('B2').format.font = {name: 'Arial', size: 16, bold: true};
    sh.getRange('B2').format.wrapText = false;
    sh.getRange(`B2:${lastCol}2`).format.rowHeightPx = 36;
    sh.getRange('B3').values = [[sheetName === 'FluxSpecification'
      ? (role === 'student' ? 'Write paired flux expressions in amber cells; label your diagram and mark each process fixed, state-dependent or residual.' : 'Completed paired amount-flux equations for notebook 03.')
      : 'Use these stable keys when reconciling your reconstruction with the model workbook.']];
    sh.getRange('B4').values = [['Teaching worksheet only. Editing this file does not change model_definition.xlsx or the simulation.']];
    sh.getRange('B5').values = [['Source: course workbook + teaching_specification.py; https://gmd.copernicus.org/articles/18/1155/2025/#section3']];
    sh.getRange('B3:B5').format.wrapText = false;
    sh.getRange(`B3:${lastCol}5`).format.rowHeightPx = 26;
    const data = [headers, ...rows.map(r => headers.map(h => r[h]))];
    sh.getRange(`B6:${lastCol}${end}`).values = data;
    sh.tables.add(`B6:${lastCol}${end}`, true, sheetName);
    const widths = sheetName === 'FluxSpecification' ? [130,220,310,170,440] : [130,320,360,430];
    widths.forEach((width, i) => {
      const col = String.fromCharCode(66 + i);
      sh.getRange(`${col}2:${col}${end}`).format.columnWidthPx = width;
    });
    sh.getRange(`B6:${lastCol}6`).format = {
      fill: role === 'student' ? '#173B61' : '#38224F',
      font: {name: 'Arial', size: 11, color: '#FFFFFF', bold: true},
      rowHeightPx: 42, wrapText: true, horizontalAlignment: 'center', verticalAlignment: 'center',
    };
    sh.getRange(`B7:${lastCol}${end}`).format.rowHeightPx = 80;
    rows.forEach((r, i) => headers.forEach((h, j) => {
      const cell = sh.getCell(i+6, j+1);
      cell.format.fill = i % 2 ? '#FFFFFF' : '#F3F7FA';
      if (r[h] === 'Your expression' || r[h] === 'Organic export: your arrow') {
        cell.values = [['']];
        cell.format.fill = '#FFF0B3';
      }
    }));
    sh.freezePanes.freezeRows(6);
    sh.freezePanes.freezeColumns(2);
    if (sheetName === 'FluxSpecification') {
      const notes = [
        'Conventions and supplied hints (symbolic equations, not Excel calculation formulas)',
        'Positive follows the arrow: subtract at source, add at destination. DIC tracks carbon even when carried as CO2 or particles.',
        'DIC_i(t), TA_i(t): mol C/kg, eq/kg. P_0 = poc_export; r = rain_ratio; W_0 = weathering_dic. d means D_b.',
        'Gas: c_i(t) = chemistry(DIC_i(t), TA_i(t); T_i, S_i, p_i); c_eq,i(t) = K0_i pCO2_atm(t). Both concentrations: mol/m3.',
        'v_i: m/yr; A_i: m2. K0_i is local solubility in compatible pressure units; p_i is water pressure, distinct from atmospheric pCO2.',
        'D(t) uses the supplied sediment response above. z_snow is sediment memory; alpha and z0 are workbook parameters. No extra sediment C stock.',
        'Fixed water mass m_i = rho_i V_i [kg]. Internal dissolved transfer: dX_i/dt = -J_X/m_i; dX_j/dt = +J_X/m_j (X = DIC or TA).',
        'Q_ij is water volume transport [m3/yr]; rho_i Q_ij converts to kg/yr. The benchmark retains its nominal litre conversion (03.3).',
        'Weathering assumes 1 mol DIC : 2 TA equivalents. Real riverine input need not have exactly this ratio.',
      ];
      notes.forEach((value, i) => {
        const row = end + 2 + i;
        sh.getRange(`B${row}`).values = [[value]];
        sh.getRange(`B${row}:${lastCol}${row}`).format = {
          font: {name:'Arial',size:11,color:'#173B61',bold:i===0},
          rowHeightPx:28, wrapText:false, verticalAlignment:'center',
        };
      });
    }
  }
  wb.recalculate();
  for (const sheetName of Object.keys(records[role])) {
    const inspect = await wb.inspect({kind: 'table', sheetId: sheetName, maxChars: 1000, tableMaxRows: 2, tableMaxCols: 3});
    console.log(role, sheetName, inspect.ndjson);
    const preview = await wb.render({sheetName, autoCrop: 'all', scale: 1, format: 'png'});
    await fs.writeFile(path.join(previewDir, `${role}_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  const errors = await wb.inspect({kind:'match', searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!', options:{useRegex:true,maxResults:20}, maxChars:1000});
  console.log(role, 'error scan', errors.ndjson);
  const xlsx = await SpreadsheetFile.exportXlsx(wb);
  await xlsx.save(path.join(outputDir, `${role}.xlsx`));
}
