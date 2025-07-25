flowchart TD
  A[Start] --> B{Is it working?}
  B -- Yes --> C[Celebrate]
  B -- No  --> D[Debug]
  D --> B

## 4. Preview & Build

1. Run `mkdocs serve`  
2. Open `http://127.0.0.1:8000/your-page/`  
3. Confirm your diagrams render and interact (zoom, pan).

When satisfied, `mkdocs build` will bake the SVGs into your `site/` folder.

---

## Advanced Tips

- To customize diagram theme or font, add Mermaid config in your `docs/extra.js`:

  ```js
  mermaid.initialize({
    theme: 'forest',
    fontFamily: 'Arial, sans-serif'
  });

