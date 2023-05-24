function applyProjectFilters(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const stadiaFilter = document.getElementById("stadiaFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;
  const inicFilter = document.getElementById("inicFilter")?.value;
  const sheffProjFilter = document.getElementById("sheffProjFilter")?.value;
  const fioInitFilter = document.getElementById('fioInitFilter')?.value;

  if (page == undefined && !fioInitFilter && !projectFilter && !stadiaFilter && !sheffProjFilter && !inicFilter && !orgFilter) {
    return;
  }
  getDataProject(page, fioInitFilter, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter);
}

function dropProjectFilter() {
  const projectFilter = document.getElementById("projectFilter");
  const stadiaFilter = document.getElementById("stadiaFilter");
  const orgFilter = document.getElementById("orgFilter");
  const inicFilter = document.getElementById("inicFilter");
  const sheffProjFilter = document.getElementById("sheffProjFilter");
  const fioInitFilter = document.getElementById('fioInitFilter');
  projectFilter && (projectFilter.value = "")
  stadiaFilter && (stadiaFilter.value = "")
  orgFilter && (orgFilter.value = "")
  inicFilter && (inicFilter.value = "")
  sheffProjFilter && (sheffProjFilter.value = "")
  fioInitFilter && (fioInitFilter.value = "")
  getDataProject(null, null, null, null, null, null, null);
}

function getDataProject(page, fioInitFilter, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/projects",
    dataSrc: "data",
    data: { page, fioInitFilter, projectFilter, stadiaFilter, orgFilter, inicFilter, sheffProjFilter },
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

function applyAssignProjectFilters(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const fioInitFilter = document.getElementById("fioInitFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;

  if (page == undefined && !projectFilter && !fioInitFilter && !orgFilter) {
    return;
  }
  getDataAssignProject(page, projectFilter, orgFilter, fioInitFilter);
}

function dropAssignProjectFilter() {
  const projectFilter = document.getElementById("projectFilter");
  const fioInitFilter = document.getElementById("fioInitFilter");
  const orgFilter = document.getElementById("orgFilter");
  projectFilter && (projectFilter.value = "")
  fioInitFilter && (fioInitFilter.value = "")
  orgFilter && (orgFilter.value = "")
  getDataAssignProject(null, null, null, null);
}

function getDataAssignProject(page, projectFilter, orgFilter, fioInitFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/assignment",
    dataSrc: "data",
    data: { page, projectFilter, orgFilter, fioInitFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function applyParticTicketsFilters(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const orgFilter = document.getElementById("orgFilter")?.value;
  const inicFilter = document.getElementById("inicFilter")?.value;
  const sheffProjFilter = document.getElementById("sheffProjFilter")?.value;

  if (page == undefined && !projectFilter && !sheffProjFilter && !inicFilter && !orgFilter) {
    return;
  }
  getDataParticTickets(page, orgFilter, inicFilter, sheffProjFilter, projectFilter);
}

function dropParticTicketsFilter() {
  const projectFilter = document.getElementById("projectFilter");
  const orgFilter = document.getElementById("orgFilter");
  const inicFilter = document.getElementById("inicFilter");
  const sheffProjFilter = document.getElementById("sheffProjFilter");
  projectFilter && (projectFilter.value = "")
  orgFilter && (orgFilter.value = "")
  inicFilter && (inicFilter.value = "")
  sheffProjFilter && (sheffProjFilter.value = "")
  getDataParticTickets(null, null, null, null, null);
}

function getDataParticTickets(page, orgFilter, inicFilter, sheffProjFilter, projectFilter) {
  $.ajax({
    type: "POST",
    url: "/student/participation_ticket",
    dataSrc: "data",
    data: { page, orgFilter, inicFilter, sheffProjFilter, projectFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
