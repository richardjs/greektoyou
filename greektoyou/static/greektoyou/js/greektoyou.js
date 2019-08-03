window.addEventListener('load', () => {
    let infoPane = document.getElementById('info-pane');
    let infoLemma = document.getElementById('info-lemma');
    let infoPOS = document.getElementById('info-pos');
    let infoParse = document.getElementById('info-parse');
    
    for (let word of document.getElementsByClassName('word')) {
        word.addEventListener('click', () => {
            infoPane.style.display = 'block';
            infoLemma.innerHTML = word.dataset.lemma;
            infoPOS.innerHTML = word.dataset.pos;
            infoParse.innerHTML = word.dataset.parse;
        });
    }

    document.body.style.display = 'block';
});
