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
