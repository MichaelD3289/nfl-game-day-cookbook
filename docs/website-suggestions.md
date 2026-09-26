# Website suggestions

Recipe, component, division and Game Day Menus pages on the website show a
suggestion prompt with two buttons:

| Button | Needs an account? | How the issue is created |
| --- | --- | --- |
| **Suggest on GitHub** | Yes | Opens a quick issue template with the page's details already filled in. The visitor submits it, so they are the issue's author. |
| **Suggest without an account** | No | Opens a form on the page. The form posts to a Google Apps Script web app that creates the issue with a bot token. |

The GitHub button always appears. The anonymous button appears only when
`suggestion_form_url` in `data/book.yml` is set.

## What each prompt suggests

| Where | Kind | Quick template | Filled in from the page |
| --- | --- | --- | --- |
| Each recipe and component page | Edit | `suggest-edit.yml` | Item name and label, source file |
| Each team card on a division page | Recipe | `quick-recipe.yml` | Team and city |
| Bottom of each division page | Recipe, dish-off | `quick-recipe.yml`, `quick-dish-off.yml` | Division (dish-off) |
| Game Day Menus page | Menu | `quick-menu.yml` | — |
| Make It or Buy It page | Component | `quick-component.yml` | — |

Only one or two fields are required for each kind. Every quick suggestion gets the
`needs-research` label and a `suggestion: <kind>` label, so you can filter them and
turn them into real tasks after research. The detailed templates (for example
`recipe-suggestion.yml`) are still there for complete write-ups.

## How anonymous issues are labelled

Issues from the form:

- get the `anonymous-suggestion` label in addition to `needs-research` and the
  kind label;
- start with a note saying the suggestion came through the website form, and who
  sent it: the name they typed, or "an anonymous visitor";
- link the GitHub username they typed, marked **unverified**. It is not
  `@mentioned`, because anyone could type any username. `@` signs in the text are
  broken up for the same reason;
- include the page they submitted from.

The form doesn't ask for an email address, and the script never sends email. A
typed GitHub username is the way to follow up with someone.

## One-time setup for the anonymous form

1. **Create the labels.** You'll do this in step 5 from the script, or create them
   by hand in **Issues → Labels**: `anonymous-suggestion`, `needs-research`,
   `suggestion: edit`, `suggestion: recipe`, `suggestion: component`,
   `suggestion: menu`, `suggestion: dish-off`. The quick templates apply these
   labels too, but GitHub only applies labels that already exist.
2. **Create a token.** On GitHub, go to **Settings → Developer settings →
   Fine-grained tokens** and create one limited to this repository, with
   **Issues: Read and write** and nothing else. Note its expiry date; the form
   stops working when it expires.
3. **Create the script.** At <https://script.google.com>, create a project and
   paste in [`website-suggestions.gs`](website-suggestions.gs).
4. **Add script properties.** In **Project settings → Script properties**:

   | Property | Value |
   | --- | --- |
   | `GITHUB_TOKEN` | The token from step 2 |
   | `REPO` | `MichaelD3289/nfl-game-day-cookbook` |

5. **Create the labels from the script** (optional). Choose `createLabels` in the
   editor and click **Run**. Approve the permissions it asks for.
6. **Deploy.** Choose **Deploy → New deployment → Web app**, with **Execute as: Me**
   and **Who has access: Anyone**. Copy the web app URL (ending in `/exec`).
   Google asks you to allow one permission, connecting to an external service
   (GitHub). The script doesn't need any other.
7. **Turn on the button.** Set `suggestion_form_url` in `data/book.yml` to that URL
   and release as usual. `make website` builds the button in locally too.

When you change the script later, use **Deploy → Manage deployments → Edit → New
version** so the URL stays the same.

## Spam and limits

- The form has a hidden honeypot field. Submissions that fill it are dropped
  silently.
- The script accepts at most 20 suggestions per hour across all visitors (change
  `MAX_PER_HOUR`) and caps each field at 5,000 characters.
- If spam becomes a problem, clear `suggestion_form_url` and release. The GitHub
  button keeps working. Revoking the token also stops the form immediately.
