function applyProjectFilters() {
  const projectFilter = document.getElementById("projectFilter").value;
  if (!projectFilter) {
    return;
  }
  getDataProject(projectFilter);
}

function dropProjectFilter() {
  getDataProject(null);
}

function getDataProject(projectFilter) {
  $.ajax({
    type: "POST",
    url: "/iniciators/projects",
    dataSrc: "data",
    data: { projectFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function uploadPassportFile(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id);
  const file = document.getElementById("input-upload" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("passport_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadPassportSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deletePassportFile(id) {
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idPassport: id },
    url: "/deletePassportSigned",
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
    },
  });
}
