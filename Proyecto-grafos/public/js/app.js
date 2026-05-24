import { api } from './api.js';
import { state } from './state.js';
import { initializeMap, renderGraph, fitToGraph } from './map.js';
import { bindDom, renderControls, renderResultSummary, loadHistory, showToast } from './ui.js';

async function bootstrap() {
  try {
    initializeMap();
    bindDom();
    const graph = await api.getGraph();
    state.graph = graph;
    renderControls();
    renderGraph();
    renderResultSummary();
    fitToGraph();
    await loadHistory();
    showToast('GeoRutas listo: grafo centrado en Zacatecas.');
  } catch (error) {
    showToast(error.message);
  }
}

bootstrap();

// ==========================================
// MÓDULO DE EXPANSIÓN DE RED (Custom Nodes)
// ==========================================

document.getElementById('btnAddNode').addEventListener('click', () => {
  const id = document.getElementById('newNodeId').value.trim().toUpperCase();
  const lat = parseFloat(document.getElementById('newNodeLat').value);
  const lng = parseFloat(document.getElementById('newNodeLng').value);

  if (!id || isNaN(lat) || isNaN(lng)) {
    showToast('Error: Ingresa un ID, Latitud y Longitud válidos.');
    return;
  }

  if (!state.graph) state.graph = { nodes: [], edges: [] };
  
  state.graph.nodes.push({ id, lat, lng });
  
  renderGraph();
  renderControls(); 
  
  showToast(`Nodo [${id}] agregado exitosamente a la red.`);
  
  document.getElementById('newNodeId').value = '';
  document.getElementById('newNodeLat').value = '';
  document.getElementById('newNodeLng').value = '';
});

document.getElementById('btnLinkNodes').addEventListener('click', () => {
  const source = document.getElementById('linkSource').value.trim().toUpperCase();
  const target = document.getElementById('linkTarget').value.trim().toUpperCase();
  const weight = parseFloat(document.getElementById('linkWeight').value);

  if (!source || !target || isNaN(weight)) {
    showToast('Error: Ingresa Origen, Destino y un Peso numérico.');
    return;
  }

  if (!state.graph) state.graph = { nodes: [], edges: [] };

  state.graph.edges.push({ 
    id: `${source}-${target}`,
    sourceId: source,  
    targetId: target,  
    distance: weight, 
    time: weight, 
    cost: weight,
    bidirectional: 1
  });
  
  renderGraph();
  renderControls();
  
  showToast(`Enlace táctico [${source} ➔ ${target}] establecido.`);
  
  document.getElementById('linkSource').value = '';
  document.getElementById('linkTarget').value = '';
  document.getElementById('linkWeight').value = '';
});

// ==========================================
// MÓDULO DE LECTURA DE DATOS TÁCTICOS (JSON)
// ==========================================

document.getElementById('graphFile').addEventListener('change', function(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  
  reader.onload = function(e) {
    try {
      const jsonGraph = JSON.parse(e.target.result);
      

      state.graph = jsonGraph;
      
      renderControls(); 
      renderGraph();    
      fitToGraph();     
      
      showToast('Datos tácticos importados y renderizados en mapa.');
      
    } catch (error) {
      console.error("Error crítico al procesar JSON:", error);
      showToast('Error: El archivo JSON está corrupto o mal estructurado.');
    }
  };
  
  reader.readAsText(file);
});

// ==========================================
// MÓDULO DE CÁLCULO Y ANÁLISIS DE DATOS
// ==========================================

document.querySelectorAll('.chip').forEach(chip => {
  chip.addEventListener('click', (event) => {
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    event.target.classList.add('active');
  });
});

document.getElementById('btnRunAlgorithm').addEventListener('click', async () => {
  const origin = document.getElementById('originSelect').value;
  const destination = document.getElementById('destinationSelect').value;
  const weightKey = document.getElementById('weightSelect').value;
  
  const activeChip = document.querySelector('.chip.active');
  const algorithm = activeChip ? activeChip.dataset.algorithm : 'dijkstra';

  if (!state.graph || !state.graph.nodes || state.graph.nodes.length === 0) {
    showToast('Alerta: Carga los datos tácticos (JSON) primero.');
    return;
  }
  if (!origin || !destination) {
    showToast('Alerta: Selecciona coordenadas de Origen y Destino.');
    return;
  }

  const btn = document.getElementById('btnRunAlgorithm');
  const originalText = btn.innerHTML;
  btn.innerText = 'PROCESANDO...';
  btn.disabled = true;

  try {
    const payload = {
      graph: state.graph,
      origin: origin,
      destination: destination,
      weight_key: weightKey,
      algorithm: algorithm
    };

    const response = await fetch('/api/algorithms/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`Error en el servidor: HTTP ${response.status}`);
    }

    const data = await response.json();

    // ==========================================
    // ACTUALIZAR EL PANEL DE ANÁLISIS (HUD)
    // ==========================================
    
    const titleObj = document.getElementById('resultTitle');
    titleObj.innerText = `MISIÓN COMPLETADA: ${algorithm.toUpperCase()}`;
    titleObj.style.color = '#0f0'; 

    document.getElementById('statCost').innerText = data.total_cost ?? data.cost ?? '0';
    document.getElementById('statVisited').innerText = data.visited_count ?? (data.path ? data.path.length : '0');
    
    const timeValue = data.execution_ms ?? data.time ?? 0;
    document.getElementById('statTime').innerText = `${parseFloat(timeValue).toFixed(2)} ms`;

    // ==========================================
    // ACTUALIZAR EL HISTORIAL DE OPERACIONES
    // ==========================================
    const historyList = document.getElementById('historyList');
    const historyItem = document.createElement('div');
    
    historyItem.style.cssText = 'background: rgba(255,255,255,0.05); padding: 10px; margin-bottom: 5px; border-left: 3px solid var(--ow-orange);';
    historyItem.innerHTML = `
      <strong style="color: var(--ow-blue);">[${algorithm.toUpperCase()}]</strong> ${origin} ➔ ${destination} <br>
      <small>Costo: ${data.total_cost ?? data.cost ?? 0} | Tiempo: ${parseFloat(timeValue).toFixed(2)} ms</small>
    `;
    
    historyList.prepend(historyItem);

    showToast('Cálculo finalizado exitosamente.');

  } catch (error) {
    console.error("Fallo crítico en el cálculo:", error);
    showToast('Fallo en el protocolo de cálculo.');
    
    const titleObj = document.getElementById('resultTitle');
    titleObj.innerText = 'ERROR EN LA OPERACIÓN';
    titleObj.style.color = 'red';
  } finally {
    btn.innerHTML = originalText;
    btn.disabled = false;
  }
});