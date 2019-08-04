window.addEventListener('load', () => {
    let infoPane = document.getElementById('info-pane');
    let infoLemma = document.getElementById('info-lemma');
    let infoPOS = document.getElementById('info-pos');
    let infoVerse = document.getElementById('info-verse');
    let infoParse = document.getElementById('info-parse');
    
    for (let word of document.getElementsByClassName('word')) {
        word.addEventListener('click', () => {
            fetch('/api/info/'+word.dataset.code).then(response => {
                return response.json();
            }).then(data => {
                infoLemma.innerHTML = data.lemma;
                infoPOS.innerHTML = data.pos;
                infoVerse.innerHTML = data.verse;
                infoParse.innerHTML = data.parse;
                infoPane.style.display = 'block';
            });
        });
    }

    document.body.style.display = 'block';
});
