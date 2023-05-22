function applyProjectFilters(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const stadiaFilter = document.getElementById("stadiaFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;
  const inicFilter = document.getElementById("inicFilter")?.value;
  const sheffProjFilter = document.getElementById("sheffProjFilter")?.value;

  if (page == undefined && !projectFilter && !stadiaFilter && !sheffProjFilter && !inicFilter && !orgFilter) {
    return;
  }
  getDataProject(page, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter);
}

function dropProjectFilter() {
  getDataProject(null, null, null, null, null, null);
}

function getDataProject(page, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/projects",
    dataSrc: "data",
    data: { page, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter },
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
  const resultDiv = document.getElementById('documents' + id);
  const button = document.getElementById("button-upload-documents" + id);
  const buttonName = button.id;
  const file = document.getElementById("input-upload-documents" + id).files[0];
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
      resultDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл загружен!'
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deletePassportFile(id) {
  const button = document.getElementById("button-delete-documents" + id)
  const buttonName = button.id;
  const resultDiv = document.getElementById('documents' + id);
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idPassport: id },
    url: "/deletePassportSigned",
    success: function (data) {
      resultDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл удален!'
    },
    error: function () {
      button.innerHTML = "Файл не удален!";
    },
  });
}

function checkStadia(id) {
  $.ajax({
    type: "GET",
    dataSrc: "data",
    data: { idProject: id },
    url: "/checkStadia",
    success: function (data) {
      const select = document.getElementById("stadia");
      select.innerHTML = "";
      if (data.IDstadiaofpr) {
        select.disabled = true;
        select.add(
          new Option(
            `${data.stadiaofprName}`,
            ''
          )
        )
      }
      else {
        select.disabled = false;
        data.map(item => {
          select.add(
            new Option(
              `${item.stadiaofprName}`,
              item.IDstadiaofpr
            )
          )
        })
      }
    },
    error: function (data) {
      console.log(data)
    }
  });
}

function uploadResultFile(id) {
  const formData = new FormData();
  const resultDiv = document.getElementById('result' + id);
  const button = document.getElementById("button-upload-result" + id);
  const buttonName = button.id;
  const file = document.getElementById("input-upload-result" + id).files[0];
  if (!file) return;
  formData.append("file", file);
  formData.append("passport_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadProjectResult",
    success: function (data) {
      resultDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл загружен!'
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteResultFile(id) {
  const button = document.getElementById("button-delete-result" + id)
  const buttonName = button.id;
  const resultDiv = document.getElementById('result' + id);
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idProject: id },
    url: "/deleteProjectResult",
    success: function (data) {
      resultDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл удален!'
    },
    error: function () {
      button.innerHTML = "Файл не удален!";
    },
  });
}

function applyAssignProjectFilters() {
  const projectFilter = document.getElementById("projectFilter").value;
  const fioInitFilter = document.getElementById("fioInitFilter").value;
  const orgFilter = document.getElementById("orgFilter").value;

  if (!projectFilter && !fioInitFilter && !orgFilter) {
    return;
  }
  getDataAssingProject(projectFilter, orgFilter, fioInitFilter);
}

function dropAssignProjectFilter() {
  getDataAssignProject(null, null, null);
}

function getDataAssignProject(projectFilter, orgFilter, fioInitFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/assignment",
    dataSrc: "data",
    data: { projectFilter, orgFilter, fioInitFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function applyParticTicketsFilters() {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;
  const inicFilter = document.getElementById("inicFilter")?.value;
  const sheffProjFilter = document.getElementById("sheffProjFilter")?.value;

  if (!projectFilter && !sheffProjFilter && !inicFilter && !orgFilter) {
    return;
  }
  getDataParticTickets(orgFilter, inicFilter, sheffProjFilter, projectFilter);
}

function dropParticTicketsFilter() {
  getDataParticTickets(null, null, null, null);
}

function getDataParticTickets(orgFilter, inicFilter, sheffProjFilter, projectFilter) {
  $.ajax({
    type: "POST",
    url: "/student/participation_ticket",
    dataSrc: "data",
    data: { orgFilter, inicFilter, sheffProjFilter, projectFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
