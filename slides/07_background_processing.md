---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} -->
## Sharing scientific tools: script to desktop application

### Background processing with Traits Futures

**Jonathan Rocher, Siddhant Wahal, Jason Chambless, Corran Webster, Prabhu Ramachandran**

**SciPy 2022**

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Traits Futures:

- Common problems with GUI frameworks:
    - GUIs are unresponsive during heavy computation
    - GUI toolkits generally require that widgets are only updated from the
      thread from which they were created
- Traits Futures solves both these problems:
    - keeping the UI responsive
    - safely update the UI in response to calculation results
- Dispatching a background task returns a `future` object which provides:
    - information about job status (e.g., job partially finished, completed,
      failed)
    - access to the job result
- Incoming results arrive as trait changes on the main thread, ensuring thread
  safety
- Supports simple callbacks, iterations, and progress-reporting functions
- Supports thread pools (default) and process pools

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Traits Futures
- Let's dive in with an example
- Installation:
    - `edm install -e ets_tutorial traits_futures`
    - Conda/pip: Activate virtual environment and `pip install traits_futures`

<!-- #endregion -->
