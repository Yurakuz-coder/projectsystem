function sendMail() {
  const admin = document.getElementById('admin').value
  const subject = document.getElementById('subject').value
  const message = document.getElementById('message').value
  const files = document.getElementById('attachedFiles').files[0]
  const button = document.getElementById('sendMailButton')
  const formData = new FormData();
  formData.append("files", files);
  formData.append("message", message);
  formData.append("subject", subject);
  formData.append("admin", admin);
  $.ajax({
    type: "POST",
    processData: false,
    contentType: false,
    data: formData,
    url: "/shefforg/sendmailtoadmin",
    success: function () {
      button.innerHTML = 'Сообщение отправлено';
    },
    error: function () {
      button.innerHTML = "Произошла ошибка при отправке!";
    },
  });
}
