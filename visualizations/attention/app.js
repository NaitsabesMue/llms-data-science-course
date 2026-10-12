/* Original teaching illustration. No runtime dependencies. Row-vector convention. */
'use strict';
const tokens = ['red', 'toy', 'robot'];
const colors = ['#b8434b', '#277c85', '#715bb4'];
const fills = ['#fbf0f0', '#eef7f7', '#f3effb'];
const X = [[1,0,0],[0,1,0],[0,0,1]];
const WQ = [[1,0],[0,1],[1,1]];
const WK = [[2,0],[0,2.3],[0,.2]];
const WV = [[1,0,0],[0,1,0],[0,0,1]];
const transpose = m => m[0].map((_, j) => m.map(row => row[j]));
const multiply = (a,b) => a.map(row => b[0].map((_,j) => row.reduce((sum,value,k) => sum + value*b[k][j],0)));
const add = (a,b) => a.map((row,i) => row.map((value,j) => value+b[i][j]));
const softmax = row => { const max=Math.max(...row); const exp=row.map(v=>Math.exp(v-max)); const total=exp.reduce((a,b)=>a+b,0); return exp.map(v=>v/total); };
const Q=multiply(X,WQ), K=multiply(X,WK), V=multiply(X,WV), KT=transpose(K);
const raw=multiply(Q,KT), scores=raw.map(row=>row.map(v=>v/Math.sqrt(2)));
const masked=scores.map((row,i)=>row.map((v,j)=>j>i?-Infinity:v));
const A=masked.map(softmax), H=multiply(A,V), Y=add(X,H);
const format = (v, digits=3) => v===-Infinity?'−∞':Number(v.toFixed(digits)).toString();
const vector = a => '['+a.map(v=>format(v)).join(', ')+']';
const percent = v => (100*v).toFixed(1)+'%';
const $ = selector => document.querySelector(selector);
const SVGNS = 'http://www.w3.org/2000/svg';
function text(x,y,content,klass='body',anchor='start',color){ return `<text x="${x}" y="${y}" class="${klass}" text-anchor="${anchor}"${color?` style="fill:${color}"`:''}>${content}</text>`; }
function rect(x,y,w,h,color='#f0f4f7',stroke='#d8e3e9',radius=9){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="${color}" stroke="${stroke}"/>`;}
function arrow(x1,y1,x2,y2,color='#7591a3',width=2,flow=false){return `<path d="M${x1},${y1} L${x2},${y2}" fill="none" stroke="${color}" stroke-width="${width}" marker-end="url(#arrow)"${flow?' class="flow"':''}/>`;}
function curve(d,color,width=2,flow=false){return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" marker-end="url(#arrow)"${flow?' class="flow"':''}/>`;}
function card(x,y,w,h,title,subtitle,color='#183044',fill='#f5f8fa'){return rect(x,y,w,h,fill,color)+text(x+w/2,y+30,title,'title','middle',color)+(subtitle?text(x+w/2,y+57,subtitle,'body','middle'): '');}
function valueCard(x,y,token,vec,w=225){const i=tokens.indexOf(token);return card(x,y,w,78,token,vector(vec),colors[i],fills[i]);}
function robot(x,y,scale=1,color='#9eabb5'){
  return `<g transform="translate(${x} ${y}) scale(${scale})"><rect x="-31" y="-30" width="62" height="44" rx="10" fill="${color}"/><rect x="-26" y="19" width="52" height="52" rx="9" fill="${color}"/><circle cx="-14" cy="-10" r="5" fill="white"/><circle cx="14" cy="-10" r="5" fill="white"/><path d="M-12 4 H12 M0 -31 V-45 M-18 72 V90 M18 72 V90 M-28 29 L-44 47 M28 29 L44 47" fill="none" stroke="${color}" stroke-width="8" stroke-linecap="round"/><circle cx="0" cy="-47" r="6" fill="${color}"/></g>`;
}
function toyRobot(x,y,scale=1){
  return `<g transform="translate(${x} ${y}) scale(${scale})"><rect x="-34" y="-38" width="68" height="49" rx="14" fill="#b8434b"/><rect x="-30" y="17" width="60" height="51" rx="14" fill="#d6545c"/><circle cx="-15" cy="-18" r="8" fill="white"/><circle cx="15" cy="-18" r="8" fill="white"/><circle cx="-15" cy="-18" r="3" fill="#183044"/><circle cx="15" cy="-18" r="3" fill="#183044"/><path d="M-12 -3 Q0 8 12 -3 M0 -39 V-52" fill="none" stroke="#183044" stroke-width="3" stroke-linecap="round"/><circle cx="0" cy="-56" r="6" fill="#f4c76b"/><circle cx="0" cy="40" r="12" fill="#f4c76b"/><path d="M-31 26 L-49 44 M31 26 L49 44 M31 52 H58" fill="none" stroke="#b8434b" stroke-width="8" stroke-linecap="round"/><path d="M58 52 C74 32 83 45 69 52 C84 58 74 72 58 52" fill="#f4c76b" stroke="#183044" stroke-width="2"/><circle cx="-20" cy="77" r="11" fill="#183044"/><circle cx="20" cy="77" r="11" fill="#183044"/><circle cx="-20" cy="77" r="4" fill="#f4c76b"/><circle cx="20" cy="77" r="4" fill="#f4c76b"/></g>`;
}
function grid(x,y,data,options={}){
  const cw=options.cw||118, rh=options.rh||47, label=options.label||'', selected=options.selected ?? -1;
  let s=text(x,y-40,label,'title');
  tokens.forEach((token,j)=>s+=text(x+125+j*cw+cw/2,y-13,token,'minor','middle',colors[j]));
  data.forEach((row,i)=>{
    s+=text(x+110,y+i*rh+rh/2+6,tokens[i],'body','end',colors[i]);
    row.forEach((v,j)=>{
      const bg = v===-Infinity?'#f8e8e8':i===selected?'#e5eff8':'#f0f4f7';
      s+=rect(x+125+j*cw,y+i*rh,cw-6,rh-5,bg,i===selected?'#17649b':'#d8e3e9',5);
      s+=text(x+125+j*cw+(cw-6)/2,y+i*rh+rh/2+5,options.perc?percent(v):format(v),'number','middle');
    });
  });
  return s;
}
const steps = [
  {label:'Purpose', title:'“toy” changes what kind of robot we mean', description:'The lookup vector for robot is the same before considering the phrase. In red toy robot, toy specifies a plaything and red adds colour. We want robot’s numerical representation to include that information.', takeaway:'Attention incorporates information from the supplied tokens. When we write prompts later, we must supply the facts and definitions needed to interpret the task.', operation:'q', scene(){
    return text(260,46,'Before context','title','middle')+text(865,46,'After context','title','middle')+robot(260,123,1.05)+toyRobot(865,135,.95)+arrow(420,130,690,130,'#17649b',3,true)+text(555,110,'Use red and toy as context','body','middle')+text(260,264,'“robot” on its own','body','middle')+text(865,264,'“robot” described as a red toy','body','middle')+text(565,312,'Pictures illustrate the interpretation, not model outputs or literal vector coordinates.','minor','middle');
  }},
  {label:'Vectors', title:'Keep the text fixed; work on its numerical representations', description:'For this short calculation, each word is one token. Each token position has an incoming vector. We collect those vectors as the rows of a matrix called X.', takeaway:'These deliberately simple vectors let us follow every calculation. A trained model uses much larger, learned vectors.', operation:'q', scene(){
    let s=text(570,40,'Incoming representations: X has 3 token rows × 3 coordinates','title','middle');
    tokens.forEach((token,i)=>{const x=85+i*345;s+=valueCard(x,93,token,X[i],280)+text(x+140,205,'Current vector x'+(i+1),'body','middle');});
    return s+text(570,273,'Attention computes an additional vector for each position, using information from allowed positions.','body','middle');
  }},
  {label:'Q / K / V', title:'Make three different views of the same incoming vector', description:'A query is used to score other positions. A key is what each position is scored against. A value contains the information that can contribute to the result. Multiplication by three learned matrices produces these views; training adjusts the matrices’ entries. One attention calculation with its own query, key, and value maps is called an attention head.', takeaway:'Q, K, and V are all calculated from the same incoming X. No token has been updated yet.', operation:'q', scene(){
    const columns=[{x:330,label:'Query',symbol:'Q = X WQ',data:Q,detail:'For scoring other positions'},{x:600,label:'Key',symbol:'K = X WK',data:K,detail:'For being scored by queries'},{x:870,label:'Value',symbol:'V = X WV',data:V,detail:'For contributing information'}];
    let s=card(25,97,195,110,'Incoming X','All three token vectors')+`<path d="M220 152 H260 V35 H992" fill="none" stroke="#7591a3" stroke-width="2"/>`;
    columns.forEach(c=>{s+=arrow(c.x+122,35,c.x+122,61,'#7591a3',2,true)+rect(c.x,61,245,228)+text(c.x+122,91,c.label,'title','middle')+text(c.x+122,119,c.symbol,'body','middle');tokens.forEach((token,i)=>s+=text(c.x+18,155+i*37,token,'minor','start',colors[i])+text(c.x+226,155+i*37,vector(c.data[i]),'body','end'));s+=text(c.x+122,270,c.detail,'minor','middle');});
    return s;
  }},
  {label:'Compare', title:'Match the “robot” query against every key', description:'A dot product multiplies matching coordinates and adds the products. A larger score here means that a value will receive more weight. The query and keys are numerical vectors, not questions or text labels.', takeaway:'We use one query (robot) three times: against the red key, the toy key, and the robot key.', operation:'scores', scene(){
    let s=card(26,104,250,93,'robot query',vector(Q[2]),colors[2],fills[2])+text(678,35,'Dot product, then divide by √2 (the query/key dimension is 2)','body','middle');
    tokens.forEach((token,i)=>{const y=65+i*78;s+=curve(`M276 150 C325 150 326 ${y+28} 360 ${y+28}`,colors[i],2,true)+card(360,y,220,60,token+' key','',colors[i],fills[i])+text(475,y+48,vector(K[i]),'minor','middle')+text(630,y+27,`1 × ${format(K[i][0])} + 1 × ${format(K[i][1])} = ${format(raw[2][i])}`,'body')+text(1035,y+27,format(scores[2][i],3),'number','middle');});
    return s+text(1035,310,'Scaled scores','minor','middle');
  }},
  {label:'All pairs', title:'One matrix multiplication calculates every query–key score', description:'Q has one query per row. Transposing K turns each key row into a column. Multiplying Q by Kᵀ takes every query–key dot product; dividing by √2 gives the scaled scores.', takeaway:'Read a row as the position receiving information, and a column as the position supplying information. The highlighted row belongs to robot.', operation:'scores', scene(){
    let s=grid(35,102,scores,{label:'Scores S = Q Kᵀ / √2',selected:2,cw:125,rh:52});
    s+=rect(660,86,440,182,'#f5f8fa')+text(683,116,'One entry, made explicit','title')+text(683,155,'robot query · toy key','body')+text(683,194,'(1 × 0 + 1 × 2.3) / √2 = 1.626','equation')+text(683,235,'Row 3, column 2','minor');
    return s+text(284,300,'Receiving position ↓','minor','middle')+text(687,300,'Supplying position →','minor','middle');
  }},
  {label:'Weights', title:'Exclude future positions, then turn scores into weights', description:'For a decoder, a position may use itself and earlier positions. Set future scores to −∞; softmax then gives them zero weight. Softmax exponentiates the allowed scores and divides by their sum, separately in each row.', takeaway:'The robot row receives 39.7% of red’s value, 49.1% of toy’s value, and 11.1% of its own value. These are not percentages of meaning.', operation:'scores', scene(){
    let s=grid(0,100,masked,{label:'Mask future positions',selected:2,cw:99,rh:50})+arrow(455,164,535,164,'#17649b',3,true)+text(494,133,'softmax','minor','middle')+grid(570,100,A,{label:'Attention weights A',selected:2,cw:112,rh:50,perc:true});
    return s+text(238,294,'Future entries are −∞ before softmax.','minor','middle')+text(865,294,'Each row sums to 100% before display rounding.','minor','middle');
  }},
  {label:'Add values', title:'Use the weights to combine value vectors', description:'A weight scales its corresponding value vector. Adding those scaled vectors gives the attention head’s output for robot. The operation for every position at once is H = A V.', takeaway:'The result is a vector to contribute at the robot position. It is not a replacement token, and it has not yet been added to robot’s original representation.', operation:'values', scene(){
    let s='';tokens.forEach((token,i)=>{const x=24+i*287;s+=valueCard(x,42,token,V[i],240)+text(x+120,158,'× '+percent(A[2][i]),'equation','middle',colors[i])+text(x+120,198,vector(V[i].map(v=>v*A[2][i])),'body','middle')+curve(`M${x+120} 213 C${x+120} 275 780 238 855 238`,colors[i],Math.max(2,A[2][i]*9),true);});
    return s+`<circle cx="874" cy="238" r="18" fill="#eef5fa" stroke="#17649b"/>`+text(874,245,'+','equation','middle')+arrow(892,238,910,238,'#17649b',2,true)+card(910,201,220,95,'Attention output',vector(H[2]),'#17649b','#eef5fa')+text(570,321,'The same weights multiply whole value vectors, coordinate by coordinate.','minor','middle');
  }},
  {label:'Residual', title:'Add the contribution to the original representation', description:'A residual connection carries the incoming vector around attention. The attention output is projected back to the representation size, then added to the original. In this example, that projection is the identity: it changes nothing.', takeaway:'robot keeps its original vector and receives an added contribution. An 11.1% self-weight does not mean that 88.9% of its original information was erased.', operation:'values', scene(){
    let s=valueCard(45,100,'robot',X[2],245)+text(168,214,'Original incoming vector','minor','middle')+text(342,152,'+','equation','middle')+card(402,100,270,78,'Attention contribution',vector(H[2]),'#17649b','#eef5fa')+text(535,214,'H Wₒ; Wₒ is identity here','minor','middle')+text(739,152,'=','equation','middle')+card(802,100,308,78,'After attention + residual',vector(Y[2]),colors[2],fills[2]);
    return s+text(570,294,'The third coordinate is 1 + 0.111…, not 0.111…. The original [0, 0, 1] remains in the sum.','body','middle');
  }},
  {label:'Every token', title:'Each position has its own query, weights, and added vector', description:'We focused on robot, but the same operations run for all token positions. The first row can only use red. The second can use red and toy. The third can use all three.', takeaway:'Token IDs and positions stay fixed. Their numerical representations change; each row has its own calculation.', operation:'values', scene(){
    let s=text(254,35,'Incoming representation','title','middle')+text(675,35,'Own attention contribution','title','middle')+text(1040,35,'After addition','title','middle');
    tokens.forEach((token,i)=>{const y=66+i*79;s+=text(33,y+31,token,'title','start',colors[i])+rect(157,y,250,55,fills[i],colors[i])+text(281,y+34,vector(X[i]),'number','middle')+text(455,y+34,'+','equation','middle')+rect(520,y,292,55,'#eef5fa','#b2cfe3')+text(666,y+34,vector(H[i]),'number','middle')+text(852,y+34,'=','equation','middle')+rect(900,y,247,55,fills[i],colors[i])+text(1023,y+34,vector(Y[i]),'number','middle');});
    return s+text(570,320,'The rows of H are different because the rows of A are different.','minor','middle');
  }},
  {label:'The block', title:'Attention is part of a Transformer block', description:'Attention combines information across token positions. A feed-forward network then processes each position’s representation separately. Both sublayers have residual additions; normalization is also used.', takeaway:'Our arithmetic covered one attention head and its residual addition. A complete block also includes feed-forward processing and normalization.', operation:'values', scene(){
    let s=card(20,140,170,80,'Input vectors','X')+card(300,140,210,80,'Self-attention','Q, K, V → H')+card(650,140,225,80,'Feed-forward','Each row separately')+card(1035,140,110,80,'Output','vectors');
    s+=arrow(190,179,300,179,'#17649b',3,true)+arrow(510,179,580,179,'#17649b',3,true)+arrow(610,179,650,179,'#17649b',3,true)+arrow(875,179,930,179,'#17649b',3,true)+arrow(970,179,1035,179,'#17649b',3,true);
    s+=curve('M225 179 V82 H595 V159','#715bb4',2,true)+curve('M628 179 V82 H950 V159','#715bb4',2,true)+text(386,67,'Carry original vector around attention','minor','middle')+text(789,67,'Carry current vector around feed-forward','minor','middle');
    [595,950].forEach(x=>s+=`<circle cx="${x}" cy="179" r="20" fill="#f3effb" stroke="#715bb4"/>`+text(x,186,'+','equation','middle'));
    return s+text(580,278,'Normalization and the combination of multiple heads are omitted from this overview.','minor','middle')+text(580,309,'The block still produces vectors at the same three token positions.','body','middle');
  }},
  {label:'Next block', title:'The next block builds fresh queries, keys, and values', description:'After the rest of the block, updated representations enter the next block. Its own learned matrices produce new Q, K, and V. It can now compare positions using representations that already contain context.', takeaway:'Within one attention step, Q, K, and V share the same incoming representations. Context changes the queries used in a later block, not halfway through the current calculation. In an application, supply the relevant facts and current tool observations to each model call.', operation:'next', scene(){
    let s=card(25,100,230,100,'Updated representations','After the complete block');
    const groups=[{y:32,title:'New queries',expr:'Q₂ = X₂ WQ,₂'},{y:129,title:'New keys',expr:'K₂ = X₂ WK,₂'},{y:226,title:'New values',expr:'V₂ = X₂ WV,₂'}];
    groups.forEach(g=>s+=curve(`M255 150 C310 150 300 ${g.y+35} 345 ${g.y+35}`,'#17649b',2,true)+card(345,g.y,330,72,g.title,g.expr));
    s+=curve('M675 68 C780 68 766 135 830 135','#715bb4',2,true)+curve('M675 165 H830','#b8434b',2,true)+card(830,95,295,115,'Compare again','New queries with new keys');
    return s+text(910,257,'Then weights → values → another addition','minor','middle');
  }}
];
const operations = [
  {id:'q',title:'Q = X WQ',description:'Multiply incoming token rows (3 coordinates) by the learned query map (3 × 2). Each resulting token row has 2 query coordinates.',left:X,right:WQ,result:Q,leftName:'X',rightName:'WQ',resultName:'Q',leftRows:tokens,leftCols:['1','2','3'],rightRows:['1','2','3'],rightCols:['1','2'],resultRows:tokens,resultCols:['1','2'],note:'Click any result entry. The highlighted input row and map column are multiplied coordinate by coordinate, then added.'},
  {id:'k',title:'K = X WK',description:'The same incoming vectors pass through a different learned map. This produces the key vectors used for comparisons.',left:X,right:WK,result:K,leftName:'X',rightName:'WK',resultName:'K',leftRows:tokens,leftCols:['1','2','3'],rightRows:['1','2','3'],rightCols:['1','2'],resultRows:tokens,resultCols:['1','2'],note:'The query map and key map are different learned parameters. Both operate on the incoming X.'},
  {id:'v',title:'V = X WV',description:'The value map produces the vectors to combine after attention weights are calculated. Here WV is the 3 × 3 identity, so V equals X.',left:X,right:WV,result:V,leftName:'X',rightName:'WV',resultName:'V',leftRows:tokens,leftCols:['1','2','3'],rightRows:['1','2','3'],rightCols:['1','2','3'],resultRows:tokens,resultCols:['1','2','3'],note:'Identity is a teaching simplification. Learned value maps in real models generally change the vectors.'},
  {id:'scores',title:'Scores = Q Kᵀ / √2',description:'K is 3 token rows × 2 coordinates. Kᵀ is 2 coordinate rows × 3 token columns. A query row times a key column computes their dot product. Divide the sum by √2.',left:Q,right:KT,result:scores,leftName:'Q',rightName:'Kᵀ',resultName:'Scores',leftRows:tokens,leftCols:['1','2'],rightRows:['1','2'],rightCols:tokens,resultRows:tokens,resultCols:tokens,scale:Math.sqrt(2),note:'Q: 3 × 2; Kᵀ: 2 × 3; scores: 3 × 3. The inner dimensions match. Receiving queries are rows; supplying keys are columns.'},
  {id:'values',title:'H = A V',description:'One row of attention weights multiplies the rows of the value matrix. Every coordinate of the output is the same weighted sum applied to that value coordinate.',left:A,right:V,result:H,leftName:'A',rightName:'V',resultName:'H',leftRows:tokens,leftCols:tokens,rightRows:tokens,rightCols:['1','2','3'],resultRows:tokens,resultCols:['1','2','3'],note:'A includes the causal mask and row-wise softmax. It weights VALUES, not original embeddings or percentages of meaning. H is the attention head output, before projection and residual addition.'},
  {id:'next',title:'Fresh maps in the next block',description:'X₂ contains the representations entering the next block, after the previous block’s attention, feed-forward processing, and normalization. The next block has different learned parameters. We have not chosen those parameters, so we show their shapes rather than inventing numerical outputs.',note:'The numerical calculations in the menu refer to the first block only. No updated query is matched against old keys within the same attention step.'}
];
const stepDuration=14000;
let step=0, playing=false, elapsed=0, lastTime=0, frame=0, operationId='q', selectedRow=2, selectedCol=0, selectedTerm=0;
let operationManuallyChosen=false;
function drawScene(){
  const svg=document.createElementNS(SVGNS,'svg');svg.setAttribute('viewBox','0 0 1160 340');svg.setAttribute('role','img');svg.setAttribute('aria-label',steps[step].title+'. '+steps[step].takeaway);
  svg.innerHTML='<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L7,3 L0,6 Z" fill="context-stroke"/></marker></defs><g class="appear">'+steps[step].scene()+'</g>';
  $('#scene').replaceChildren(svg);
}
function render(){
  $('#step-number').textContent=`Step ${step+1} of ${steps.length}`;$('#step-title').textContent=steps[step].title;$('#step-description').textContent=steps[step].description;$('#takeaway').textContent=steps[step].takeaway;$('#counter').textContent=`${step+1} / ${steps.length}`;
  $('#back').disabled=step===0;$('#next').disabled=step===steps.length-1;
  document.querySelectorAll('#stages button').forEach((button,i)=>{button.classList.toggle('active',i===step);button.classList.toggle('done',i<step);if(i===step)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');});
  if(!operationManuallyChosen){operationId=steps[step].operation;$('#operation').value=operationId;selectedRow=2;selectedCol=operationId==='scores'?1:0;selectedTerm=0;}
  drawScene();renderMath();
}
function matrixMarkup(data,name,rowLabels,colLabels,role){
  let html=`<div class="matrix-wrap"><div class="matrix-title">${name}</div><div class="matrix-shape">${data.length} rows × ${data[0].length} columns</div><table class="matrix" aria-label="${name} matrix"><thead><tr><th></th>${colLabels.map(label=>`<th class="label" scope="col">${label}</th>`).join('')}</tr></thead><tbody>`;
  data.forEach((row,i)=>{html+=`<tr><th class="label" scope="row">${rowLabels[i]}</th>`;row.forEach((v,j)=>{
    let klass='';if(role==='result')klass+=' selectable'+(i===selectedRow&&j===selectedCol?' selected':'');
    if(role==='left'&&i===selectedRow)klass+=' source';if(role==='right'&&j===selectedCol)klass+=' source';
    if(role==='left'&&i===selectedRow&&j===selectedTerm)klass+=' term';if(role==='right'&&j===selectedCol&&i===selectedTerm)klass+=' term';
    html+=`<td><button class="${klass}" data-role="${role}" data-row="${i}" data-col="${j}"${role!=='result'?' tabindex="-1"':''} aria-label="${name}, row ${rowLabels[i]}, column ${colLabels[j]}: ${format(v,6)}">${format(v)}</button></td>`;
  });html+='</tr>';});return html+'</tbody></table></div>';
}
function renderMath(){
  const op=operations.find(o=>o.id===operationId);
  $('#math-title').textContent=op.title;$('#math-description').textContent=op.description;$('#math-note').textContent=op.note;
  $('#product-next').disabled=op.id==='next';
  if(op.id==='next'){
    $('#matrices').innerHTML=['Q','K','V'].map(symbol=>`<div class="matrix-wrap"><div class="matrix-title">${symbol}₂ = X₂ W${symbol},₂</div><div class="matrix-shape">(3 × 3) × (3 × ${symbol==='V'?3:2}) → (3 × ${symbol==='V'?3:2})</div></div>`).join('<span class="operator">·</span>');
    $('#products').textContent='All three new maps take X₂. New Q₂ and K₂ are compared; new V₂ supplies the information to combine.';return;
  }
  selectedCol=Math.min(selectedCol,op.result[0].length-1);selectedTerm=Math.min(selectedTerm,op.left[0].length-1);
  $('#matrices').innerHTML=matrixMarkup(op.left,op.leftName,op.leftRows,op.leftCols,'left')+'<span class="operator" aria-hidden="true">×</span>'+matrixMarkup(op.right,op.rightName,op.rightRows,op.rightCols,'right')+(op.scale?'<span class="operator" aria-hidden="true">/ √2</span>':'')+'<span class="operator" aria-hidden="true">=</span>'+matrixMarkup(op.result,op.resultName,op.resultRows,op.resultCols,'result');
  const terms=op.left[selectedRow].map((value,k)=>`<span${k===selectedTerm?' class="active-term"':''}>${format(value,4)} × ${format(op.right[k][selectedCol],4)}</span>`);
  const subtotal=op.left[selectedRow].slice(0,selectedTerm+1).reduce((sum,value,k)=>sum+value*op.right[k][selectedCol],0);
  $('#products').innerHTML=`<strong>${op.resultName}[${op.resultRows[selectedRow]}, ${op.resultCols[selectedCol]}]</strong> = ${op.scale?'(' : ''}${terms.join(' + ')}${op.scale?') / √2' : ''} ≈ <strong>${format(op.result[selectedRow][selectedCol],4)}</strong><br><span class="minor">Highlighted product ${selectedTerm+1}/${terms.length}; accumulated dot-product sum through this product: ${format(subtotal,4)}${op.scale?' (before scaling)':''}. Displayed numbers are rounded; calculations use full precision.</span>`;
  document.querySelectorAll('#matrices button.selectable').forEach(button=>button.addEventListener('click',()=>{selectedRow=Number(button.dataset.row);selectedCol=Number(button.dataset.col);selectedTerm=0;renderMath();}));
}
function setStep(next){step=Math.max(0,Math.min(steps.length-1,next));elapsed=0;$('#progress').value=0;operationManuallyChosen=false;render();}
function setPlaying(value){playing=value;document.body.classList.toggle('playing',value);$('#play').textContent=value?'❚❚ Pause':'▶ Play';$('#play').setAttribute('aria-pressed',String(value));lastTime=0;cancelAnimationFrame(frame);if(value)frame=requestAnimationFrame(tick);}
function tick(time){
  if(!playing)return;if(lastTime)elapsed+=(time-lastTime)*Number($('#speed').value);lastTime=time;$('#progress').value=Math.min(100,100*elapsed/stepDuration);
  const op=operations.find(o=>o.id===operationId), term=op.left?Math.floor(elapsed/1700)%op.left[0].length:0;if(term!==selectedTerm&& !$('#math').hidden){selectedTerm=term;renderMath();}
  if(elapsed>=stepDuration){if(step===steps.length-1){setPlaying(false);return;}setStep(step+1);}
  frame=requestAnimationFrame(tick);
}
steps.forEach((item,i)=>{const button=document.createElement('button');button.textContent=`${i+1}. ${item.label}`;button.addEventListener('click',()=>setStep(i));$('#stages').append(button);});
operations.forEach(op=>{const option=document.createElement('option');option.value=op.id;option.textContent=op.title;$('#operation').append(option);});
$('#back').addEventListener('click',()=>setStep(step-1));$('#next').addEventListener('click',()=>setStep(step+1));$('#play').addEventListener('click',()=>{if(!playing&&step===steps.length-1)setStep(0);setPlaying(!playing);});
$('#speed').addEventListener('change',()=>document.documentElement.style.setProperty('--speed',$('#speed').value));
$('#show-math').addEventListener('change',event=>{ $('#math').hidden=!event.target.checked; });
$('#operation').addEventListener('change',event=>{operationId=event.target.value;operationManuallyChosen=true;selectedRow=2;selectedCol=operationId==='scores'?1:0;selectedTerm=0;renderMath();});
$('#product-next').addEventListener('click',()=>{const op=operations.find(o=>o.id===operationId);if(op.left){selectedTerm=(selectedTerm+1)%op.left[0].length;renderMath();}});
document.addEventListener('keydown',event=>{if(/^(INPUT|SELECT|BUTTON|SUMMARY|A)$/.test(event.target.tagName)||event.ctrlKey||event.metaKey||event.altKey)return;if(event.key==='ArrowRight'){event.preventDefault();setStep(step+1);}if(event.key==='ArrowLeft'){event.preventDefault();setStep(step-1);}if(event.code==='Space'){event.preventDefault();setPlaying(!playing);}});
document.addEventListener('visibilitychange',()=>{if(document.hidden)setPlaying(false);});
const initialOptions=new URLSearchParams(location.search);
const initialStep=Number(initialOptions.get('step')||1);
if(Number.isFinite(initialStep))step=Math.max(0,Math.min(steps.length-1,Math.trunc(initialStep)-1));
if(initialOptions.get('math')==='1'){$('#show-math').checked=true;$('#math').hidden=false;}
render();
