/**
 * Files anonymous cookbook-website suggestions as GitHub issues.
 *
 * Deploy as a Google Apps Script web app (Execute as: Me, Who has access: Anyone).
 * Setup and script properties are described in docs/website-suggestions.md.
 * Issue sections and title prefixes mirror the quick issue templates in
 * .github/ISSUE_TEMPLATE/, so both paths produce issues that look the same.
 */

var KINDS = {
  edit: {
    title: 'Edit suggestion: ', titleField: 'item', label: 'suggestion: edit',
    fields: [['item', 'Recipe or component', true], ['change', 'What should change?', true],
             ['why', 'Why? (optional)'], ['page', 'Source file (optional)']]
  },
  recipe: {
    title: 'Recipe idea: ', titleField: 'dish', label: 'suggestion: recipe',
    fields: [['team', 'Team', true], ['dish', 'Dish name or idea', true],
             ['details', 'Anything else? (optional)']]
  },
  component: {
    title: 'Component idea: ', titleField: 'name', label: 'suggestion: component',
    fields: [['name', 'Component name or idea', true], ['details', 'Anything else? (optional)']]
  },
  menu: {
    title: 'Menu idea: ', titleField: 'idea', label: 'suggestion: menu',
    fields: [['idea', 'Menu idea', true], ['details', 'Anything else? (optional)']]
  },
  'dish-off': {
    title: 'Dish-off idea: ', titleField: 'division', label: 'suggestion: dish-off',
    fields: [['division', 'Division', true], ['idea', 'Dish-off idea', true],
             ['details', 'Anything else? (optional)']]
  }
};

var ANONYMOUS_LABEL = 'anonymous-suggestion';
var LABELS = {
  'anonymous-suggestion': ['d4c5f9', 'Sent from the website form without a GitHub account'],
  'needs-research': ['fbca04', 'Quick suggestion to research before it becomes a task'],
  'suggestion: edit': ['c5def5', 'Fix or improve an existing recipe or component'],
  'suggestion: recipe': ['c2e0c6', 'New recipe idea'],
  'suggestion: component': ['c2e0c6', 'New Make It or Buy It component idea'],
  'suggestion: menu': ['c2e0c6', 'New game-day menu idea'],
  'suggestion: dish-off': ['c2e0c6', 'New division dish-off idea']
};
var MAX_PER_HOUR = 20;
var MAX_FIELD = 5000;

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    if (data.website) return reply({ ok: true }); // honeypot: pretend success to bots
    var kind = KINDS[data.kind];
    if (!kind) return reply({ ok: false, error: 'unknown suggestion type' });
    var fields = data.fields || {};
    for (var i = 0; i < kind.fields.length; i++) {
      var spec = kind.fields[i];
      if (spec[2] && !clean(fields[spec[0]])) return reply({ ok: false, error: 'missing ' + spec[1] });
    }
    if (!withinRateLimit()) return reply({ ok: false, error: 'too many suggestions, try later' });
    var issue = createIssue(kind, fields, data.from || {}, clean(data.page, 500));
    return reply({ ok: true, url: issue.html_url });
  } catch (err) {
    console.error(err);
    return reply({ ok: false, error: 'could not file the suggestion' });
  }
}

function createIssue(kind, fields, from, page) {
  var name = clean(from.name, 100);
  var github = clean(from.github, 39);
  if (!/^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$/.test(github)) github = '';
  var who = name ? '**' + noMentions(name) + '**' : 'an anonymous visitor';
  if (github) who += ' (GitHub, unverified: [' + github + '](https://github.com/' + github + '))';

  var body = ['> [!NOTE]',
              '> Submitted **anonymously** through the website suggestion form by ' + who + '.'];
  body.push('> Research before turning this into a task.');
  kind.fields.forEach(function (spec) {
    body.push('', '### ' + spec[1], '', noMentions(clean(fields[spec[0]])) || '_No response_');
  });
  if (page) body.push('', '### Website page', '', page);

  var subject = clean(fields[kind.titleField], 80).replace(/\s+/g, ' ');
  var response = github_('post', '/issues', {
    title: kind.title + noMentions(subject),
    body: body.join('\n'),
    labels: [ANONYMOUS_LABEL, 'needs-research', kind.label]
  });
  return JSON.parse(response.getContentText());
}

function withinRateLimit() {
  var cache = CacheService.getScriptCache();
  var lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    var count = Number(cache.get('count') || 0);
    if (count >= MAX_PER_HOUR) return false;
    cache.put('count', String(count + 1), 3600);
    return true;
  } finally {
    lock.releaseLock();
  }
}

function github_(method, path, payload) {
  var props = PropertiesService.getScriptProperties();
  var response = UrlFetchApp.fetch('https://api.github.com/repos/' + props.getProperty('REPO') + path, {
    method: method,
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + props.getProperty('GITHUB_TOKEN'),
      Accept: 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28'
    },
    payload: payload ? JSON.stringify(payload) : undefined,
    muteHttpExceptions: true
  });
  var code = response.getResponseCode();
  if (code >= 300 && !(path === '/labels' && code === 422)) {
    throw new Error('GitHub ' + code + ': ' + response.getContentText());
  }
  return response;
}

/** Run once from the editor: creates the labels used by both suggestion paths. */
function createLabels() {
  Object.keys(LABELS).forEach(function (name) {
    github_('post', '/labels', { name: name, color: LABELS[name][0], description: LABELS[name][1] });
  });
}

function clean(value, max) {
  return String(value || '').trim().slice(0, max || MAX_FIELD);
}

// Anonymous text must not ping people: break up @mentions.
function noMentions(text) {
  return text.replace(/@/g, '@​');
}

function reply(result) {
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
