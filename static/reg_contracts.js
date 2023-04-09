function applyContractsFilters() {
  const dateContractFilter = document.getElementById("dateContractFilter").value;
  const orgFilters = document.getElementById("orgFilter").value;
  const numberContractFilter = document.getElementById("numberContractFilter").value;
  if (!dateContractFilter && !orgFilters && !numberContractFilter) {
    return;
  }
  getData(dateContractFilter, orgFilters, numberContractFilter)
}

function dropContractFilters() {
  getData(null, null, null)
}

function getData(dateContractFilter, orgFilters, numberContractFilter) {
  $.ajax({
    type: "POST",
    url: "/admin/contracts",
    dataSrc: "data",
    data: { dateContractFilter, orgFilters, numberContractFilter },
    success: function (data) {
      const table = document.getElementById("collapseTableBody")
      table.innerHTML = data;
      table.className = 'collapse show'
    },
    error: function (err) {
      console.log(err)
    },
  });
}

function uploadFile(id) {
  const formData = new FormData();
  const file = document.getElementById(id)
  formData.append("file", file)
  $.ajax({
    type: 'POST',
    files: file,
    body: formData,
    headers: {
      "Content-Type": file.contentType
    },
  })
}
