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

function applyStudApprovedTicketsFilters() {
  const projectFioFilter = document.getElementById("projectFioFilter").value;
  const projectNameFilter = document.getElementById("projectNameFilter").value;
  const groupFilter = document.getElementById("grname").value;
  if (!projectFioFilter && !projectNameFilter && !groupFilter) {
    return;
  }
  getStudApprovedTicketsData(projectFioFilter, projectNameFilter, groupFilter);
}

function dropStudApprovedTicketsFilter() {
  getStudApprovedTicketsData(null, null, null);
}

function getStudApprovedTicketsData(projectFioFilter, projectNameFilter, groupFilter) {
  $.ajax({
    type: "POST",
    url: "/sheffproj/approved_tickets",
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

function uploadConfirmation(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id);
  const file = document.getElementById("input-upload" + id).files[0];
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
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteConfirmation(id) {
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idConfirmation: id },
    url: "/deleteConfirmation",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
  });
}
