# Contributing

Help us make a cookbook that feels like eating in each NFL city. Local knowledge,
cooking experience, corrections, and well-sourced recipe suggestions are welcome.

## Suggest content without coding

Contributions are welcome across the whole cookbook. Choose a form:

| Contribution | What to include |
| --- | --- |
| [Recipe](https://github.com/MichaelD3289/nfl-game-day-cookbook/issues/new?template=recipe-suggestion.yml) | Team/city, local connection, recipe source, and cooking experience |
| [Make It or Buy It component](https://github.com/MichaelD3289/nfl-game-day-cookbook/issues/new?template=component-suggestion.yml) | Homemade sauce, dip, topping, seasoning, side, staple, or protein; recipes using it; and a good buy-it alternative |
| [Division dish-off](https://github.com/MichaelD3289/nfl-game-day-cookbook/issues/new?template=division-dish-off.yml) | A menu using dishes from one division, why they pair well, and a prep note |
| [Game-day menu](https://github.com/MichaelD3289/nfl-game-day-cookbook/issues/new?template=game-day-menu.yml) | Grudge Match Grub, Shared Prep, Across the League, Premium Day, Fast Day, or Budget Day |

Fun names, regional expertise, practical prep ideas, and improvements to existing
content are all welcome. Link existing dishes where possible. If a menu needs a new
recipe or component, open a linked suggestion for that item too. Photos are optional;
you do not need to install tools to contribute an idea.

## Submit a pull request

1. Fork the repository and make a branch from current `main`.
2. Keep one recipe, component, menu, or coherent change per PR. Read [AGENTS.md](AGENTS.md).
3. Install [uv](https://docs.astral.sh/uv/) and run `uv sync --locked`.
4. Use the appropriate starter and guide below. Paths determine the team, division,
   component kind, or menu type; use IDs from the project’s `data/` files.
5. New content starts as a draft until editorial review. Do not invent metadata fields.
6. Run `make check`. If you have Quarto/TinyTeX, also run `make pdf` and `make website`
   for published content/layout changes. Otherwise ask for maintainer build help.
7. Add visible changes to `CHANGELOG.md` under Unreleased. Open a PR using a descriptive
   Conventional Commit title, for example `feat(bills): add a regional appetizer`.

Do not edit `generated/` or `dist/`. Do not bump versions or create tags; maintainers
prepare releases and automation tags them after merging. Documentation-only changes
can remain Unreleased without rebuilding the cookbook.

## Content starters and authoring guides

| Content | Starter or format guide | Destination |
| --- | --- | --- |
| Recipe | `uv run nfl-book new recipe --team bills --slug your-dish`; [recipe format](.claude/skills/add-recipe/SKILL.md) | `recipes/<conf>/<division>/<team>/<id>.md` |
| Component | `uv run nfl-book new component --kind sauces --slug your-sauce`; [component format](.claude/skills/add-component/SKILL.md) | `components/<kind>/<id>.md` |
| Division dish-off | Copy the division YAML example in the [menu guide](.claude/skills/menus-and-dish-offs/SKILL.md); set `status: draft` | `menus/divisions/<conf>/<division>/<id>.yml` |
| Game-day menu | Copy the game-day YAML example in the [menu guide](.claude/skills/menus-and-dish-offs/SKILL.md); set `status: draft` | `menus/game-day/<type>/<id>.yml` |

For every file, `id` must match its filename. Menu recipe lists contain recipe IDs,
not page numbers or URLs. Published menus can reference only published recipes.
Division dish-offs should use their own division. Keep card descriptions concise.
For Grudge Match Grub, represent both teams; for shared prep, explain exactly what
can be prepared once and used twice. Fast/budget claims need realistic assumptions.
Components use `## From Scratch`, not recipe `## Instructions`, and are linked from
recipe ingredient lines with `{{component:id}}`.

## Recipe review expectations

- Explain the connection to the city with evidence. Regional variants are welcome
  when clearly named and explained.
- Preserve authentic technique. Faster methods are optional shortcuts, not replacements.
- Match ingredient quantities and instructions to the cited source; identify adaptations.
- Specify otherwise ambiguous ingredients (sauce style, beer type, cheese, cut of meat)
  where it affects the dish. Brand recommendations should be optional and explained.
- Use numbered, actionable steps, realistic yield/timing, and clear doneness cues.
- Consider homemade sauces, slaws, seasonings, and dips with useful buy-it alternatives.
- Use full canonical source URLs. A maintainer can populate short links before publication;
  do not replace existing cached short links.

## Text, photos, and attribution

Submit original writing/photos or material you have permission to redistribute.
Link to reference recipes instead of copying their prose or images without permission.
In your PR, record each image's creator, source URL, license or written permission,
and required credit. Use the supported `photo_credit` field for the displayed credit;
put permission evidence in the PR, not a new unrecognized front-matter field.
Never submit private permission correspondence publicly without the sender's consent.
Existing source credits do not certify that reuse permissions have been audited.

## Contribution licensing

By submitting original software or developer documentation for inclusion, you agree
to license it under [MIT](LICENSE). Original cookbook text and images are contributed
under [CC BY 4.0](LICENSE-CONTENT.md). Only contribute material you can license on those
terms, or clearly identify third-party material and its compatible reuse permission.
You retain your copyright. See [THIRD_PARTY.md](THIRD_PARTY.md) for required evidence.

## Review and safety

Outside-contributor workflows need maintainer approval. The `Validate` check runs lint,
tests, and content validation with read-only repository access and no project secrets.
It does not build the complete PDF or website; maintainers verify output-affecting changes
before merging. Do not approve an unfamiliar workflow change without reading it.

Be constructive and follow [our code of conduct](CODE_OF_CONDUCT.md).
Report vulnerabilities through [SECURITY.md](SECURITY.md), not a public issue.
