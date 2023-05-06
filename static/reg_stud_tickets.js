function applyStudTicketsFilters() {
  const projectFioFilter = document.getElementById("projectFioFilter").value;
  const projectNameFilter = document.getElementById("projectNameFilter").value;
  if (!projectFioFilter && !projectNameFilter) {
    return;
  }
  getStudTicketsData(projectFioFilter, projectNameFilter);
}

function dropStudTicketsFilter() {
  getStudTicketsData(null, null);
}

function getStudTicketsData(projectFioFilter, projectNameFilter) {
  $.ajax({
    type: "POST",
    url: "/sheffproj/tickets",
    dataSrc: "data",
    data: { projectFioFilter, projectNameFilter },
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
  if (!projectFioFilter && !projectNameFilter) {
    return;
  }
  getStudApprovedTicketsData(projectFioFilter, projectNameFilter);
}

function dropStudApprovedTicketsFilter() {
  getStudApprovedTicketsData(null, null);
}

function getStudApprovedTicketsData(projectFioFilter, projectNameFilter) {
  $.ajax({
    type: "POST",
    url: "/sheffproj/approved_tickets",
    dataSrc: "data",
    data: { projectFioFilter, projectNameFilter },
    success: function (data) {
      const accordion = document.getElementById("projectsAccordion");
      accordion.innerHTML = data;
    },
    error: function (err) {
      console.log(err);
    },
  });
}
