function uploadWork(id) {
  const formData = new FormData();
  const button = document.getElementById("button-upload" + id)
  const buttonName = button.id;
  const file = document.getElementById("input-upload" + id).files[0];
  const workDiv = document.getElementById("work" + id);
  if (!file) return;
  formData.append("file", file);
  formData.append("work_id", id);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/uploadWorkStudent",
    success: function (data) {
      workDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл загружен!'
    },
    error: function () {
      button.innerHTML = "Файл не загружен!";
    },
  });
}

function deleteWork(id) {
  const button = document.getElementById("button-delete" + id)
  const buttonName = button.id;
  const workconfirmedDiv = document.getElementById("work" + id);
  $.ajax({
    type: "POST",
    dataSrc: "data",
    data: { idWork: id },
    url: "/deleteWorkStudent",
    success: function (data) {
      workconfirmedDiv.innerHTML = data
      document.getElementById(buttonName).innerHTML = 'Файл удален!'
    },
    error: function () {
      button.innerHTML = "Файл не удален!";
    },
  });
}

function applyInicWorkFilters(page) {
  const fioFilter = document.getElementById("fioFilter")?.value;
  const projectFilter = document.getElementById("projectFilter")?.value;
  const roleFilter = document.getElementById("roleFilter")?.value;
  const statusFilter = document.getElementById("status")?.value;

  if (page == undefined && !projectFilter && !fioFilter && !roleFilter && !statusFilter) {
    return;
  }
  getDataInicWorkProject(page, projectFilter, fioFilter, roleFilter, statusFilter);
}

function dropInicWorkFilter() {
  const fioFilter = document.getElementById("fioFilter");
  const projectFilter = document.getElementById("projectFilter");
  const roleFilter = document.getElementById("roleFilter");
  const statusFilter = document.getElementById("status");
  fioFilter && (fioFilter.value = "")
  projectFilter && (projectFilter.value = "")
  roleFilter && (roleFilter.value = "")
  statusFilter && (statusFilter.value = "")

  getDataInicWorkProject(null, null, null, null, null);
}

function getDataInicWorkProject(page, projectFilter, fioFilter, roleFilter, statusFilter) {
  const url = window.location.pathname.split('/')[1]
  $.ajax({
    type: "POST",
    url: "/" + url + "/works",
    dataSrc: "data",
    data: { page, projectFilter, fioFilter, roleFilter, statusFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}


function getRolesProjects(id) {
  $.ajax({
    type: "GET",
    dataSrc: "data",
    data: { idProject: id },
    url: "/getRolesProjects",
    success: function (data) {
      const select = document.getElementById("idrole");
      select.innerHTML = "";
      if (data.length == 0) {
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
              `${item.rolesRole} - ${item.rolesFunction}`,
              item.IDroles
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
