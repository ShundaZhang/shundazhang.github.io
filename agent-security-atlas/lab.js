(() => {
  const lab = document.getElementById('policy-lab');
  const scenario = lab.querySelector('select');
  const description = document.getElementById('scenario-description');
  const verdict = document.getElementById('verdict');
  const title = verdict.querySelector('strong');
  const reason = verdict.querySelector('p');
  const missing = document.documentElement.lang === 'zh-CN'
    ? '当前情境所需的检查已关闭：'
    : 'The control for this scenario is off: ';

  function update() {
    const selected = scenario.selectedOptions[0];
    const control = document.getElementById(selected.dataset.control);
    const label = control.closest('label').textContent.trim();
    description.textContent = selected.dataset.description;
    verdict.dataset.allowed = String(!control.checked);
    title.textContent = control.checked ? verdict.dataset.pass : verdict.dataset.fail;
    reason.textContent = control.checked ? label : missing + label;
  }

  lab.addEventListener('change', update);
  update();
})();
