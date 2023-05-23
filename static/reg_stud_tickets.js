function applyStudTicketsFilters() {
  const projectFioFilter = document.getElementById("projectFioFilter").value;
  const projectNameFilter = document.getElementById("projectNameFilter").value;
  const groupFilter = document.getElementById("grname").value;
  if (!projectFioFilter && !projectNameFilter && !groupFilter) {
    return;
  }
  getStudTicketsData(projectFioFilter, projectNameFilter, groupFilter);
}

function dropStudTicketsFilter() {
  getStudTicketsData(null, null, null);
}

function getStudTicketsData(projectFioFilter, projectNameFilter, groupFilter) {
  $.ajax({
    type: "POST",
    url: "/sheffproj/tickets",
    dataSrc: "data",
    data: { projectFioFilter, projectNameFilter, groupFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function applyStudApprovedTicketsFilters(page) {
  const projectFioFilter = document.getElementById("projectFioFilter").value;
  const projectNameFilter = document.getElementById("projectNameFilter").value;
  const groupFilter = document.getElementById("grname").value;
  if (page == undefined && !projectFioFilter && !projectNameFilter && !groupFilter) {
    return;
  }
  getStudApprovedTicketsData(page, projectFioFilter, projectNameFilter, groupFilter);
}

function dropStudApprovedTicketsFilter() {
  const projectFioFilter = document.getElementById("projectFioFilter");
  const projectNameFilter = document.getElementById("projectNameFilter");
  const groupFilter = document.getElementById("grname");
  projectFioFilter && (projectFioFilter.value = "")
  projectNameFilter && (projectNameFilter.value = "")
  groupFilter && (groupFilter.value = "")
  getStudApprovedTicketsData(null, null, null, null);
}

function getStudApprovedTicketsData(page, projectFioFilter, projectNameFilter, groupFilter) {
  $.ajax({
    type: "POST",
    url: "/sheffproj/approved_tickets",
    dataSrc: "data",
    data: { page, projectFioFilter, projectNameFilter, groupFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadConfirmation(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id)
  const buttonName = button.id;
  const file = document.getElementById("input-upload" + id).files[0];
  const confirmedDiv = document.getElementById("confirmed" + id);
  if (!file) return;
  formData.append("file", file);
  formData.append("confirmation_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadConfirmation",
    success: function (data) {
      confirmedDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл загружен!'
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteConfirmation(id) {
  const button = document.getElementById("button-delete" + id)
  const buttonName = button.id;
  const confirmedDiv = document.getElementById("confirmed" + id);
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idConfirmation: id },
    url: "/deleteConfirmation",
    success: function (data) {
      confirmedDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл удален!'
    },
    error: function () {
      button.innerHTML = "Файл не удален!";
    },
  });
}
