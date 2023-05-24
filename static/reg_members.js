function applyMembersFilters(page) {
  const projectFioFilter = document.getElementById("projectFioFilter")?.value;
  const projectRoleFilter = document.getElementById("projectRoleFilter")?.value;
  const projectNaprFilter = document.getElementById("projectNaprFilter")?.value;
  const groupFilter = document.getElementById("grname")?.value;
  const statusFilter = document.getElementById("status")?.value;

  if (page == undefined && !statusFilter && !projectFioFilter && !projectRoleFilter && !projectNaprFilter && !groupFilter) {
    return;
  }
  getDataMembers(page, statusFilter, projectFioFilter, projectRoleFilter, projectNaprFilter, groupFilter);
}

function dropMembersFilter() {
  const projectFioFilter = document.getElementById("projectFioFilter");
  const projectRoleFilter = document.getElementById("projectRoleFilter");
  const projectNaprFilter = document.getElementById("projectNaprFilter");
  const groupFilter = document.getElementById("grname");
  const statusFilter = document.getElementById("status");
  projectFioFilter && (projectFioFilter.value = "")
  projectRoleFilter && (projectRoleFilter.value = "")
  groupFilter && (groupFilter.value = "")
  statusFilter && (statusFilter.value = "")
  projectNaprFilter && (projectNaprFilter.value = "")
  getDataMembers(null, null, null, null, null, null);
}

function getDataMembers(
  page, statusFilter, projectFioFilter, projectRoleFilter, projectNaprFilter, groupFilter
) {
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    url: "/" + url + "/members",
    dataSrc: "data",
    data: { page, statusFilter, projectFioFilter, projectRoleFilter, projectNaprFilter, groupFilter },
    success: function (data) {
      const accordion = document.getElementById("membersAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function getCompetitionsSpec(id, operation) {
  $.ajax({
    type: "GET",
    dataSrc: "data",
    data: { id },
    url: "/getCompetitionsSpec",
    success: function (data) {
      const checkboxes = document.getElementById(operation + "Wrapper");
      const elements = document.querySelectorAll(
        "#" + operation + 'Wrapper input[type="checkbox"]:checked'
      );
      let checkboxData = "";
      for (el of elements) {
        checkboxData += `<div class="form-check">${el.outerHTML.replace(
          ">",
          " checked>"
        )}${el.nextElementSibling.outerHTML}</div>`;
      }
      for (el of data) {
        if (
          !elements.length ||
          !document.getElementById(`add_spec_${el[0]}_${id}`)
        )
          checkboxData += `<div class="form-check">
          <input class="form-check-input" name="comp" type="checkbox" value="${el[0]}"
            id="add_spec_${el[0]}_${id}">
          <label class="form-check-label" for="add_spec_${el[0]}_${id}">
            ${el[1]} - ${el[2]}
          </label>
          </div>`;
      }
      if (checkboxData == "") checkboxData = "<p>Данных не найдено</p>";
      checkboxes.innerHTML = checkboxData;
    },
  });
}

function applyRolesFilters(page) {
  const projectFilter = document.getElementById("projectFilter")?.value;
  const opopFilter = document.getElementById("opopFilter")?.value;
  const projectRoleFilter = document.getElementById("projectRoleFilter")?.value;

  if (page == undefined && !projectFilter && !projectRoleFilter && !opopFilter) {
    return;
  }
  getDataRoles(page, projectFilter, projectRoleFilter, opopFilter);
}

function dropRolesFilter() {
  const projectFilter = document.getElementById("projectFilter");
  const opopFilter = document.getElementById("opopFilter");
  const projectRoleFilter = document.getElementById("projectRoleFilter");
  projectFilter && (projectFilter.value = "")
  opopFilter && (opopFilter.value = "")
  projectRoleFilter && (projectRoleFilter.value = "")
  getDataRoles(null, null, null, null);
}

function getDataRoles(
  page, projectFilter, projectRoleFilter, opopFilter
) {
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    url: "/" + url + "/roles",
    dataSrc: "data",
    data: { page, projectFilter, projectRoleFilter, opopFilter },
    success: function (data) {
      const accordion = document.getElementById("membersAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function applyMemFilters(page) {
  const projectFioFilter = document.getElementById("projectFioFilter")?.value;
  const projectNameFilter = document.getElementById("projectNameFilter")?.value;
  const groupFilter = document.getElementById("grname")?.value;
  const roleFilter = document.getElementById("roleFilter")?.value;
  const naprFilter = document.getElementById("naprFilter")?.value;
  const statusFilter = document.getElementById('status')?.value;

  if (page == undefined && !groupFilter && !roleFilter && !projectFioFilter && !projectNameFilter && !naprFilter && !statusFilter) {
    return;
  }
  getDataMem(page, roleFilter, groupFilter, projectFioFilter, projectNameFilter, naprFilter, statusFilter);
}

function dropMemFilter() {
  const projectFioFilter = document.getElementById("projectFioFilter");
  const projectNameFilter = document.getElementById("projectNameFilter");
  const groupFilter = document.getElementById("grname");
  const roleFilter = document.getElementById("roleFilter");
  const naprFilter = document.getElementById("naprFilter");
  const statusFilter = document.getElementById('status');
  projectFioFilter && (projectFioFilter.value = "")
  projectNameFilter && (projectNameFilter.value = "")
  groupFilter && (groupFilter.value = "")
  roleFilter && (roleFilter.value = "")
  naprFilter && (naprFilter.value = "")
  statusFilter && (statusFilter.value = "")
  getDataMem(null, null, null, null, null, null, null);
}

function getDataMem(
  page, roleFilter, groupFilter, projectFioFilter, projectNameFilter, naprFilter, statusFilter
) {
  const url = window.location.pathname.split("/")[1];
  $.ajax({
    type: "POST",
    url: "/" + url + "/members",
    dataSrc: "data",
    data: { page, roleFilter, groupFilter, projectFioFilter, projectNameFilter, naprFilter, statusFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
