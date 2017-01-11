checkInput = function(inputId, hrefId){
  element = document.getElementById(inputId)

  element.addEventListener('input', function(){
    target = document.getElementById(hrefId)
    value = element.value
    if(value.length == 0){
      currentHref = target.href
      newHref = currentHref.split("?")[0]
      target.href = newHref

      currentText = target.text
      newText = currentText.split("?")[0]
      target.text = newText
    }else{
      currentHref = target.href
      newHref = currentHref.split("?")[0]
      newHref += "?limit=" + value
      target.href = newHref

      currentText = target.text
      newText = currentText.split("?")[0]
      newText += "?limit=" + value
      target.text = newText
    }
  })
}

document.addEventListener('DOMContentLoaded', checkInput("song_limit--input", "song_limit--href"), false);
