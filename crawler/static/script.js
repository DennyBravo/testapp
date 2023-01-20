const setLoaderVisibility = (visible) => {
  const loader = document.querySelector('#mainLoader');

  if (visible) {
    loader.classList.add('visible')
  } else {
    loader.classList.remove('visible')
  }
}

const setFormState = (state) => {
  const formFields = document.querySelector('#form > fieldset');

  if (state) {
    formFields?.removeAttribute('disabled')
  } else {
    formFields?.setAttribute('disabled', 'disabled')
  }
}

const setCounter = (value) => {
  const counter = document.querySelector('#resultsCounter');

  counter.innerHTML = value === null ? '' : `Found ${value} links`
}

const sorter = (a, b) => a.linked_page > b.linked_page ? 1 : -1;

const renderData = (data) => {
  const container = document.querySelector('#table-container tbody');
  const rows = data.sort(sorter).reduce((acc, item) => acc + `
      <tr>
        <td>${item.is_internal ? 'Yes' : ''}</td>
        <td>${item.is_page_anchor ? 'Yes' : ''}</td>
        <td>
          <div style="width: 700px;">${item.linked_page}${item.anchor || ''}</div>
        </td>
      <tr>`.trim(), '');
  container.innerHTML = rows;
}

const sendRequest = (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form)
  const data = new URLSearchParams(formData)

  setFormState(false);
  setLoaderVisibility(true);
  setCounter(null);
  renderData([])

  fetch('/api/parse/', {
    method: 'post',
    body: data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    },
  })
    .then(response => response.json())
    .then((data) => {
      renderData(data);
      setCounter(data.length)
    })
    .finally(() => {
      setFormState(true);
      setLoaderVisibility(false);
    });
}

document.getElementById('form')?.addEventListener('submit', sendRequest);
