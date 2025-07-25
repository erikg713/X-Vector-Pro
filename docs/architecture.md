%%{init: {"theme": "forest", "fontFamily": "Arial, sans-serif"}}%%
flowchart LR
  subgraph UI Layer
    GUI[GUI Tab]
    CLI[CLI Interface]
  end

  subgraph Entry Points
    GUI --> Controller[Controller / Scheduler]
    CLI --> ArgParser[ArgParser / CLI Parser]
    ArgParser --> Controller
  end

  subgraph Core Modules
    Controller --> Recon[Recon Module]
    Controller --> Scan[Scan Module]
    Controller --> Brute[Brute Module]
    Controller --> CVE[CVE Module]
  end

  Recon --> Exploit[Exploit Runner]
  Scan  --> Exploit
  Brute --> Exploit
  CVE   --> Exploit

  Exploit --> Reports[Report Generator]
