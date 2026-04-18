// 1. CONFIGURAÇÃO DO SLIDE HERO (Visual)
const slides = [
    { img: "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200", frase: "O seu futuro profissional começa aqui." },
    { img: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200", frase: "Conectando talentos em todo Moçambique." },
    { img: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200", frase: "Sua carreira não tem limites no MozWorks." }
];

let slideAtual = 0;
function rodarSlides() {
    const hero = document.getElementById('hero-section');
    const frase = document.getElementById('frase-motivadora');
    if (hero && frase) {
        hero.style.backgroundImage = `url('${slides[slideAtual].img}')`;
        frase.innerText = slides[slideAtual].frase;
        slideAtual = (slideAtual + 1) % slides.length;
    }
}
setInterval(rodarSlides, 5000);
rodarSlides();

// 2. VARIÁVEIS GLOBAIS
const container = document.getElementById('containerVagas');
const inputBusca = document.getElementById('inputBusca');
const selectProvincia = document.getElementById('selectProvincia');
let todasAsVagas = []; // Lista que será preenchida pelo JSON do GitHub

// 3. FUNÇÃO PARA DESENHAR AS VAGAS NA TELA
function renderVagas(dados) {
    container.innerHTML = "";
    if (!dados || dados.length === 0) {
        container.innerHTML = "<p style='text-align:center; padding: 20px;'>Nenhuma vaga encontrada no momento.</p>";
        return;
    }

    dados.forEach(vaga => {
        const html = `
            <div class="card-vaga">
                <div class="vaga-info">
                    <h3>${vaga.titulo}</h3>
                    <p><strong>Empresa:</strong> ${vaga.empresa}</p>
                    <p><strong>Província:</strong> ${vaga.provincia}</p>
                </div>
                <a href="${vaga.link}" target="_blank" class="btn-vaga">Ver Detalhes</a>
            </div>
        `;
        container.innerHTML += html;
    });
}

// 4. FUNÇÃO DE FILTRO (Pesquisa e Província)
function filtrar() {
    const busca = inputBusca.value.toLowerCase();
    const provincia = selectProvincia.value;

    const filtrados = todasAsVagas.filter(vaga => {
        const tituloOK = vaga.titulo.toLowerCase().includes(busca);
        const provinciaOK = provincia === "" || vaga.provincia === provincia;
        return tituloOK && provinciaOK;
    });

    renderVagas(filtrados);
}

// 5. O SEGREDO DA AUTOMAÇÃO: BUSCAR O FICHEIRO DO TEU GITHUB
async function buscarVagasDoGitHub() {
    // URL apontando para o ficheiro que o Python vai atualizar no teu repositório
    const url = "https://raw.githubusercontent.com/BasilioDona/mozworks/main/vagas.json";

    try {
        const resposta = await fetch(url);
        if (!resposta.ok) throw new Error("Ficheiro não encontrado");
        
        todasAsVagas = await resposta.json();
        renderVagas(todasAsVagas);
    } catch (erro) {
        console.error("Erro ao carregar vagas:", erro);
        container.innerHTML = `
            <div style="text-align:center; padding: 20px;">
                <p>O robô MozWorks está a preparar as primeiras vagas...</p>
                <small>Verifica se o ficheiro vagas.json já existe no teu GitHub.</small>
            </div>`;
    }
}

// Ouvir os campos de pesquisa
inputBusca.addEventListener('input', filtrar);
selectProvincia.addEventListener('change', filtrar);

// Iniciar o site
buscarVagasDoGitHub();
