import { useMemo, useState, useEffect } from 'react';
import { TOOL_CATEGORIES, ToolItem, ToolCategory } from './data/tools';

type RunState = {
  isOpen: boolean;
  tool?: ToolItem;
  progressPercent: number;
  etaSeconds: number;
  startedAtMs: number | null;
};

export function App() {
  const [query, setQuery] = useState('');
  const [run, setRun] = useState<RunState>({ isOpen: false, progressPercent: 0, etaSeconds: 0, startedAtMs: null });

  const flatTools = useMemo(() => TOOL_CATEGORIES.flatMap(c => c.tools.map(t => ({ ...t, categoryId: c.id }))), []);

  const filteredCategories: ToolCategory[] = useMemo(() => {
    if (!query.trim()) return TOOL_CATEGORIES;
    const q = query.toLowerCase();
    return TOOL_CATEGORIES.map(cat => ({
      ...cat,
      tools: cat.tools.filter(t =>
        t.name.toLowerCase().includes(q) ||
        t.subtitle.toLowerCase().includes(q) ||
        t.tags.some(tag => tag.toLowerCase().includes(q))
      )
    })).filter(cat => cat.tools.length > 0);
  }, [query]);

  useEffect(() => {
    if (!run.isOpen || !run.tool) return;
    let animationFrame = 0;
    const duration = run.tool.processingSeconds;
    const start = performance.now();
    const tick = (now: number) => {
      const elapsed = (now - start) / 1000;
      const pct = Math.min(99, Math.floor((elapsed / duration) * 100));
      const eta = Math.max(0, Math.ceil(duration - elapsed));
      setRun(prev => ({ ...prev, progressPercent: pct, etaSeconds: eta }));
      if (elapsed < duration) {
        animationFrame = requestAnimationFrame(tick);
      } else {
        setRun(prev => ({ ...prev, progressPercent: 100, etaSeconds: 0 }));
      }
    };
    animationFrame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(animationFrame);
  }, [run.isOpen, run.tool]);

  function onRun(tool: ToolItem) {
    setRun({ isOpen: true, tool, progressPercent: 0, etaSeconds: tool.processingSeconds, startedAtMs: Date.now() });
  }
  function onClose() {
    setRun({ isOpen: false, progressPercent: 0, etaSeconds: 0, startedAtMs: null, tool: undefined });
  }

  return (
    <div className="container">
      <header className="header">
        <div className="brand">
          <div className="logo" />
          <h1>ToolSaaS · 105 Tools</h1>
        </div>
        <div className="search">
          <input
            placeholder="Search tools (e.g. PDF, Excel, Image, SEO, AI, URL)"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
        <div className="kbd">⌘K</div>
      </header>

      <div className="sections">
        {filteredCategories.map(cat => (
          <section className="category" key={cat.id} id={cat.id}>
            <div className="category-header">
              <div className="category-title">
                <h2>{cat.title}</h2>
                <span className="pill">{cat.tools.length} tools</span>
              </div>
              <span className="pill">Modern · Realtime · Responsive</span>
            </div>
            <div className="grid">
              {cat.tools.map(tool => (
                <article className="card" key={tool.id}>
                  <h3>{tool.name}</h3>
                  <p>{tool.subtitle}</p>
                  <div className="meta">
                    <span>⏱ {tool.processingSeconds}s</span>
                    <span>•</span>
                    <span>{tool.output}</span>
                  </div>
                  <div className="actions">
                    <button className="btn primary" onClick={() => onRun(tool)}>Open</button>
                    <button className="btn secondary" disabled>Docs</button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        ))}
      </div>

      {run.isOpen && run.tool && (
        <div className="modal-backdrop" role="dialog" aria-modal>
          <div className="modal">
            <header>
              <strong>{run.tool.name}</strong>
              <button className="btn" onClick={onClose}>Close</button>
            </header>
            <div className="content">
              <div className="row">
                <span className="subhead">Processing</span>
                <span>{run.progressPercent}%</span>
              </div>
              <div className="progress"><span style={{ width: `${run.progressPercent}%` }} /></div>
              <div className="row">
                <span>Estimated time remaining</span>
                <span>{run.etaSeconds}s</span>
              </div>
              <p className="meta">Simulated realtime progress. Backend integration ready.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
