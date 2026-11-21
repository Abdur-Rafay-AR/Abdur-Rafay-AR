<p align="center">
  <img src="banner.svg" alt="Abdur Rafay - AI Systems &amp; Infrastructure" width="100%" />
</p>

<p align="center">
  <a href="https://abdur-rafay-ar.github.io/" target="_blank">
    <img src="https://img.shields.io/badge/Portfolio-Visit-141718?style=flat-square&logo=googlechrome&logoColor=white&labelColor=08090a" alt="Portfolio" />
  </a>
  &nbsp;
  <a href="https://linkedin.com/in/abdur-rafay-ar" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Connect-141718?style=flat-square&logo=linkedin&logoColor=white&labelColor=08090a" alt="LinkedIn" />
  </a>
  &nbsp;
  <a href="https://www.upwork.com/freelancers/~01e0e53ea3fc415198" target="_blank">
    <img src="https://img.shields.io/badge/Upwork-Hire-141718?style=flat-square&logo=upwork&logoColor=white&labelColor=08090a" alt="Upwork" />
  </a>
  &nbsp;
  <a href="mailto:abdurrafay.tech@gmail.com">
    <img src="https://img.shields.io/badge/Email-Contact-141718?style=flat-square&logo=gmail&logoColor=white&labelColor=08090a" alt="Email" />
  </a>
</p>

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## About

I'm Abdur Rafay, an AI Engineer based in Islamabad. I design and ship multi-agent systems and agent infrastructure: autonomous planning loops, local time-travel debugging, persistent memory, and real-time voice pipelines. I own the CI/CD and cloud stack underneath them too.

Most AI work fails somewhere other than the prompt: in state drift across agents, in unobservable tool loops, in a blocking call that adds half a second to a phone conversation, or in the deploy that nobody automated. I work on that whole surface, not just the model call.

- Author of **Athar**, **Relay**, and **ai-cache** on PyPI.
- Focus: Multi-agent systems, local-first agent infrastructure, and real-time voice AI.
- Infrastructure ownership: CI/CD automation, Docker, AWS, and Google Cloud stacks.
- Engineering background across six international roles (formerly Member of Technical Staff at Lythe Labs).
- Undergraduate AI Researcher completing a BS in Artificial Intelligence at Bahria University (BUIC E-8).
- Available for freelance contracts and full-time engineering roles.

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## Published on PyPI &amp; Core Systems

| Project | Type | Description | Stack | Links |
|:---|:---:|:---|:---|:---:|
| **Athar** | PyPI | Local-first, time-travel debugger and observability engine for multi-agent LLM systems with SQLite WAL, state mutation, and instantaneous fork &amp; replay. | Python, FastAPI, SQLite WAL, LangGraph | [Source](https://github.com/Abdur-Rafay-AR/athar) &middot; [PyPI](https://pypi.org/project/athar/) |
| **Relay** | PyPI | MCP server that audits Python voice-agent codebases for async mistakes and blocking calls that quietly add latency to a phone call via AST analysis. | Python, MCP, AST Analysis, asyncio | [Source](https://github.com/arclat-ai/relay-mcp) &middot; [PyPI](https://pypi.org/project/relay-arclat/) |
| **ai-cache** | PyPI | Transparent local caching of LLM responses across OpenAI, Anthropic, and Gemini via SQLite to cut latency and API token spend. | Python, SQLite, LLM APIs | [Source](https://github.com/Abdur-Rafay-AR/ai-cache) &middot; [PyPI](https://pypi.org/project/ai-cache/) |
| **Crucible** | OSS | Multi-agent framework that runs entirely on-machine: hybrid BM25 + embedding retrieval over SQLite, local models via Ollama, zero core dependencies. | Python, SQLite, Ollama, BM25 | [Source](https://github.com/Abdur-Rafay-AR/crucible) |
| **Voice Agent Starter Kit** | OSS | Complete real-time voice loop streaming ASR &rarr; LLM &rarr; TTS over WebSockets with client-side VAD, barge-in, and built-in latency telemetry. | FastAPI, WebSockets, Deepgram, Groq | [Source](https://github.com/lythelab/voice-agent-starter-kit) |
| **mcpie** | OSS | Security scanner for MCP servers in the shape of npm audit. Scans for tool poisoning, over-broad permissions, and credential exposure. | TypeScript, MCP, Static Analysis | [Source](https://github.com/arclat-ai/mcpie) |
| **Agent Testing Suite** | OSS | Interactive evaluation dashboard for multi-agent pipelines: instruments latency, token spend, and tool invocation frequency. | Python, LangChain, Streamlit | [Source](https://github.com/lythelab/agent-testing-suite) |
| **Long-Running Agent** | OSS | Autonomous agent built for weeks of continuous runtime: LLM planning loops, sandboxed execution, and resumable sessions. | Python, LangChain, FastAPI | [Source](https://github.com/lythelab/autonomous-agent) |

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## Upstream Contributions

- **[arize-ai/phoenix](https://github.com/Arize-ai/phoenix)** (11.4k+ stars): Added the production `GET /v1/model_providers` REST endpoint with pagination, auth scoping, automated OpenAPI schema generation, and full pytest regression coverage.
- **[docling-project/docling-core](https://github.com/docling-project/docling-core)** (IBM): Exposed JSON serialization kwargs (`ensure_ascii`, `sort_keys`) in `save_as_json` with unit test suites covering non-ASCII encoding guarantees.

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## Toolkit

<p align="left">
  <b>Languages</b><br/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/SQL-CC292B?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/C++-00599C?style=flat-square&logo=cplusplus&logoColor=white" />
</p>

<p align="left">
  <b>AI, LLMs &amp; Agents</b><br/>
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white" />
  <img src="https://img.shields.io/badge/MCP-08090a?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-F55036?style=flat-square&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Anthropic-19C37D?style=flat-square&logo=anthropic&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/RAG%20Pipelines-1C3C3C?style=flat-square" />
</p>

<p align="left">
  <b>Backend &amp; Real-Time</b><br/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/WebSockets-010101?style=flat-square&logo=socketdotio&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-FF6F61?style=flat-square" />
</p>

<p align="left">
  <b>Cloud, DevOps &amp; QA</b><br/>
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/CI%2FCD-08090a?style=flat-square&logo=githubactions&logoColor=white" />
</p>

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## Credentials

<table>
  <tr>
    <td width="150" align="center">
      <a href="https://www.credly.com/badges/75a6c244-0709-4b7e-85ea-2d826e1b9c86/public_url" target="_blank">
        <img src="https://images.credly.com/images/70675aed-31be-4c30-add7-b99905a34005/linkedin_thumb_image.png" alt="IBM AI Developer Professional Certificate" width="120" />
      </a>
    </td>
    <td>
      <h3>IBM AI Developer Professional Certificate</h3>
      <p>Demonstrated proficiency in building, training, and deploying AI models, generative AI integrations, and full-stack Python/Flask applications.</p>
      <a href="https://www.credly.com/users/abdur-rafay.658ecb38" target="_blank">
        <b>Verify on Credly &rarr;</b>
      </a>
    </td>
  </tr>
</table>

- **AI Infrastructure &amp; Operations Fundamentals**: NVIDIA
- **Generative AI with Large Language Models**: AWS &amp; DeepLearning.AI
- **Supervised Machine Learning: Regression &amp; Classification**: Stanford &amp; DeepLearning.AI

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

## Activity

<div align="center">
  <img src="stats/top-languages.svg" alt="Top Languages" width="41%" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="stats/activity.svg" alt="GitHub Activity" width="51%" />
</div>

<p align="center"><img src="divider.svg" width="100%" alt="" /></p>

<p align="center">
  <a href="https://abdur-rafay-ar.github.io/" target="_blank">Portfolio</a> &nbsp;&middot;&nbsp;
  <a href="https://linkedin.com/in/abdur-rafay-ar" target="_blank">LinkedIn</a> &nbsp;&middot;&nbsp;
  <a href="https://www.upwork.com/freelancers/~01e0e53ea3fc415198" target="_blank">Upwork</a> &nbsp;&middot;&nbsp;
  <a href="https://medium.com/@abdurrafay432007" target="_blank">Medium</a> &nbsp;&middot;&nbsp;
  <a href="https://abdur-rafay-ar.github.io/resume/" target="_blank">Résumé</a> &nbsp;&middot;&nbsp;
  <a href="mailto:abdurrafay.tech@gmail.com">Contact</a>
</p>
