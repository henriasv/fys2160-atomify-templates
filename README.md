# FYS2160 Atomify examples

➡️ **https://andeplane.github.io/atomify/?examplesUrl=https://raw.githubusercontent.com/henriasv/fys2160-atomify-templates/main/examples.json&screen=examples**

Molecular dynamics examples for *FYS2160 Thermal and statistical physics*, run
in the browser with [Atomify](https://github.com/andeplane/atomify). Each
example is a folder with a LAMMPS input script, a Jupyter notebook for the
analysis, and a thumbnail:

| Example | Folder |
| --- | --- |
| My first MD simulation | [`my-first-md-simulation/`](my-first-md-simulation) |
| Melting of a 2D solid | [`2d-melting/`](2d-melting) |
| Heat capacity of LJ | [`heat-capacity-lj/`](heat-capacity-lj) |
| 3D diffusion MSD | [`3d-msd-diffusion/`](3d-msd-diffusion) |

The examples are the *startup* set from [dysthe/atomify](https://github.com/dysthe/atomify),
ported to the current Atomify (the July 2026 rewrite with persistent projects,
run history and a shared Jupyter filesystem).

## How an example is used in Atomify

1. Open the link above and pick an example. **Quick run** runs it immediately in a
   scratch project; **Use as project** creates a project in the browser's storage.
2. Every run of a project is kept under `runs/run-001/`, `runs/run-002/`, … with
   a snapshot of the input files, `log.lammps` and any dump files.
3. The **Notebook** tab opens the example's notebook with the project directory
   as working directory. The notebooks here load the newest run with
   `glob("runs/*/log.lammps")`.

Only share links of the form `?examplesUrl=…`. Parameters such as
`&project=diffusion&tab=files` that Atomify adds while you work are deep links
into *your* browser's project storage and do nothing for anybody else.

## `examples.json`

```jsonc
{
  "baseUrl": "https://raw.githubusercontent.com/henriasv/fys2160-atomify-templates/main",
  "title": "...",                    // heading of the example library
  "descriptionFile": "description.md",  // markdown shown above the examples
  "examples": [
    {
      "id": "2d-melting",            // unique, lower-case
      "title": "Melting of a 2D solid",
      "description": "...",          // shown on the card
      "imageUrl": "2d-melting/2d-melting.jpg",
      "inputScript": "2d-melting.in",     // must match one files[].fileName
      "keywords": ["phase transitions", "lennard jones"],  // keywords[0] is the card label
      "files": [
        { "fileName": "2d-melting.in",    "url": "2d-melting/2d-melting.in" },
        { "fileName": "2d-melting.ipynb", "url": "2d-melting/2d-melting.ipynb" }
      ]
    }
  ]
}
```

Every `url` and `imageUrl` is fetched as `{baseUrl}/{url}`, so paths are
relative to the repository root. Project creation is all-or-nothing: if a
single file returns 404, neither Quick run nor Use as project works for that
example.

Things that differ from the older
[atomify-examples-template](https://github.com/andeplane/atomify-examples-template)
format and from dysthe/atomify:

- **No `analysisScript`.** Atomify now fetches `{baseUrl}/{analysisScript}`
  when creating the project. A bare file name such as `"2d-melting.ipynb"`
  resolves to the repository root, 404s, and the example cannot be opened at
  all. Listing the notebook under `files` is sufficient: a project that ships a
  notebook uses it instead of the generated `analysis.ipynb`.
- **Notebooks read `runs/*/log.lammps`**, not `log.lammps`. The notebook's
  working directory is the project directory; LAMMPS runs inside the run
  directory.
- **`%pip install lammps-logfile`** replaces the old `sys.path.append('/drive')`
  hack. The wheel is bundled with Atomify, so this works offline.

## Adding an example

1. Create a folder `<id>/` with `<id>.in`, `<id>.ipynb` and a thumbnail.
   Keep thumbnails small (JPEG, ≲ 300 kB): they are loaded for every card.
2. Add an entry to `examples.json` (copy an existing one).
3. Run `python check_examples.py`. It checks that every referenced file exists,
   that `inputScript` is in `files`, and that notebooks follow the `runs/`
   layout. The same check runs in GitHub Actions on every push.
4. After pushing, `python check_examples.py --remote` requests every published
   URL to confirm the raw.githubusercontent.com links resolve.

### Notebook skeleton

```python
%pip install -q lammps-logfile pandas
```
```python
import glob
import lammps_logfile
import matplotlib.pyplot as plt

logs = sorted(glob.glob("runs/*/log.lammps"))   # every run of this project
log = lammps_logfile.File(logs[-1])             # newest run
print(log.get_keywords())
```

## Local development

Edit `examples.json` so `baseUrl` is `http://localhost:8000`, start

```
python server.py
```

and open
https://andeplane.github.io/atomify/?examplesUrl=http://localhost:8000/examples.json&screen=examples.

Recent Chrome versions ask for permission before a public site may talk to
`localhost` ("Local Network Access"); if Atomify silently shows its default
library, look for that prompt in the address bar and allow it, then reload.
Remember to change `baseUrl` back before committing (`check_examples.py`
warns while it points at localhost).
