function applyGroupsMembers() {
  const group = document.getElementById("group").value;
  if (!group) {
    return;
  }
  getDataGroupsMembers(group);
}

function getDataGroupsMembers(group) {
  $.ajax({
    type: "POST",
    url: "/admin/group-members",
    dataSrc: "data",
    data: { group },
    success: function (data) {
      const table = document.getElementById("collapseTableBody");
      table.innerHTML = data;
      table.className = "collapse show";
    },
    error: function (err) {
      console.log(err);
    },
  });
}

function getStudentsGroup(idGroup, op) {
  $.ajax({
    type: "GET",
    url: "/admin/getStudentsGroup",
    data: { idGroup },
    success: function (data) {
      const select = document.getElementById(op + "Student");
      const button = document.getElementById(op + "ModalButton");
      select.innerHTML = "";
      if (!data.length) {
        select.add(new Option("Студенты не найдены", 0));
        button.disabled = true;
        select.disabled = true;
        return;
      }
      select.disabled = false;
      button.disabled = false;
      for (let item of data) {
        select.add(
          new Option(
            `${item.FullName} #${item.studentsStudbook}`,
            item.IDstudents
          )
        );
      }
    },
    error: function (err) {
      console.log(err);
    },
  });
}
