(function(){
  function byId(id){ return document.getElementById(id); }

  function initToolPage(){
    if (typeof window.TOOL_SLUG === 'undefined') return;
    const uploadForm = byId('uploadForm');
    const fileInput = byId('fileInput');
    const startBtn = byId('startBtn');
    const progressBar = byId('progressBar');
    const progressText = byId('progressText');
    const downloadSection = byId('downloadSection');
    const downloadLink = byId('downloadLink');

    function setProgress(pct, message){
      progressBar.style.width = pct + '%';
      progressText.textContent = message + ' (' + pct + '%)';
    }

    startBtn && startBtn.addEventListener('click', async function(){
      downloadSection.classList.add('hidden');
      setProgress(0, 'Uploading...');
      const fd = new FormData(uploadForm);
      try {
        const up = await fetch('/api/tools/' + window.TOOL_SLUG + '/upload', { method: 'POST', body: fd });
        const upJson = await up.json();
        if (!up.ok || upJson.error){
          setProgress(0, 'Upload failed');
          return;
        }
      } catch(e){
        setProgress(0, 'Upload error');
        return;
      }

      setProgress(0, 'Starting...');
      const es = new EventSource('/api/tools/' + window.TOOL_SLUG + '/progress');
      es.onmessage = function(ev){
        try {
          const data = JSON.parse(ev.data);
          if (data.status === 'running'){
            setProgress(data.progress || 0, data.message || 'Processing');
          } else if (data.status === 'started'){
            setProgress(0, data.message || 'Queued');
          } else if (data.status === 'completed'){
            setProgress(100, data.message || 'Done');
            if (data.download_url){
              downloadLink.href = data.download_url;
              downloadSection.classList.remove('hidden');
            }
            es.close();
          }
        } catch(e){ /* ignore */ }
      };
      es.onerror = function(){ es.close(); };
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    initToolPage();
  });
})();