// 1. CONFIGURAÇÃO DO SLIDE (HERO)
const slides = [
    { img: "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200", frase: "O seu futuro profissional começa aqui." },
    { img: "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200", frase: "Conectando talentos em todo Moçambique." }
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

// 2. VARIÁVEIS GLOBAIS
let todasAsVagas = [];
let indiceCarrossel = 0;
let intervaloCarrossel;
const sheetId = '1vuTCvVpxefyl3UBP1KI14Pm7x7jYnQdBYUgxLPPNtO4';

// FUNÇÃO DE LIMPEZA (Versão mais leve para não quebrar o layout)
function filtrarTexto(str) {
    if (!str) return "";
    return String(str).replace(/<[^>]*>?/gm, ''); // Remove apenas tags HTML suspeitas
}

// 3. FUNÇÃO PARA DESENHAR O CARROSSEL (Soluções Profissionais)
function renderCarrossel(dados) {
    const track = document.getElementById('carrosselServicos');
    if (!track) return;
    track.innerHTML = "";

    if (dados.length === 0) {
        track.innerHTML = "<p style='color:#666; padding:20px;'>Sem soluções disponíveis.</p>";
        return;
    }

    dados.forEach(item => {
        const foto = (item.fotoCapa && item.fotoCapa.trim() !== "") 
            ? item.fotoCapa 
            : 'https://images.unsplash.com/photo-1454165833762-02305732f83f?auto=format&fit=crop&w=300&q=80';

        track.innerHTML += `
            <div class="carrossel-item">
                <div class="img-servico" style="background-image: url('${foto}')"></div>
                <div class="conteudo-servico">
                    <h4>${filtrarTexto(item.titulo)}</h4>
                    <p>${filtrarTexto(item.empresa)}</p>
                    <a href="${item.link}" target="_blank" class="btn-servico-sm">Saber Mais</a>
                </div>
            </div>
        `;
    });

    iniciarMovimentoAutomatico(dados.length);
}

function iniciarMovimentoAutomatico(total) {
    const track = document.getElementById('carrosselServicos');
    if (!track || total <= 1) return;
    if (intervaloCarrossel) clearInterval(intervaloCarrossel);
    intervaloCarrossel = setInterval(() => {
        indiceCarrossel++;
        if (indiceCarrossel >= total) indiceCarrossel = 0;
        track.style.transform = `translateX(-${indiceCarrossel * 300}px)`;
    }, 4000);
}

// 4. FUNÇÃO PARA DESENHAR A LISTA DE VAGAS
function renderListaVagas(dados) {
    const container = document.getElementById('containerVagas');
    const contadorTexto = document.getElementById('totalVagasSemana');
    
    if (!container) return;
    container.innerHTML = "";

    // Atualiza o contador de vagas real
    if (contadorTexto) contadorTexto.innerText = `+${dados.length}`;

    if (dados.length === 0) {
        container.innerHTML = "<p style='text-align:center; padding:40px; grid-column: 1/-1;'>Nenhuma vaga encontrada.</p>";
        return;
    }

    dados.forEach(vaga => {
        const linkOriginal = vaga.link ? String(vaga.link).trim() : "";
        const linkTeste = linkOriginal.toLowerCase();
        
        let textoBotao = "Ver Detalhes";
        let linkFinal = linkOriginal;
        let classeCor = "btn-vaga";
        let acaoExtra = "";

        if (linkTeste === "" || linkTeste === "#" || linkTeste === "físico") {
            textoBotao = "Ver Instruções";
            linkFinal = "javascript:void(0)";
            classeCor += " btn-aviso";
            acaoExtra = `onclick="alert('Verifique os detalhes no título para se candidatar.')"`;
        } else if (linkTeste.match(/\.(jpeg|jpg|png|webp)$/i)) {
            textoBotao = "Ver Edital";
            classeCor += " btn-imagem";
        } else if (linkTeste.includes("wa.me")) {
            textoBotao = "WhatsApp";
            classeCor += " btn-whatsapp";
        }

        container.innerHTML += `
            <div class="card-vaga">
                <div class="vaga-info">
                    <h3>${filtrarTexto(vaga.titulo)}</h3>
                    <p><strong>Empresa:</strong> ${filtrarTexto(vaga.empresa)}</p>
                    <p><strong>Província:</strong> ${filtrarTexto(vaga.provincia)}</p>
                </div>
                <a href="${linkFinal}" target="_blank" class="${classeCor}" ${acaoExtra}>
                    ${textoBotao}
                </a>
            </div>
        `;
    });
}

// 5. FILTRO DE BUSCA
function filtrarVagas() {
    const busca = document.getElementById('inputBusca').value.toLowerCase();
    const prov = document.getElementById('selectProvincia').value.toLowerCase();
    const filtrados = todasAsVagas.filter(v => {
        const termo = (v.titulo + v.empresa).toLowerCase();
        return termo.includes(busca) && (prov === "" || v.provincia.toLowerCase() === prov);
    });
    renderListaVagas(filtrados);
}

// 6. CARREGAR DADOS DO GOOGLE SHEETS
async function carregarDados() {
    const urlVagas = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tqx=out:json&sheet=Página1`;
    const urlServicos = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tqx=out:json&sheet=Página2`;

    try {
        const [resV, resS] = await Promise.all([fetch(urlVagas), fetch(urlServicos)]);
        
        const txtV = await resV.text();
        const jsonV = JSON.parse(txtV.substring(47).slice(0, -2));
        todasAsVagas = jsonV.table.rows.slice(1).map(r => ({
            titulo: r.c[0]?.v || "", 
            empresa: r.c[1]?.v || "",
            provincia: r.c[2]?.v || "", 
            link: r.c[3]?.v || ""
        }));

        const txtS = await resS.text();
        const jsonS = JSON.parse(txtS.substring(47).slice(0, -2));
        const listaServicos = jsonS.table.rows.slice(1).map(r => ({
            titulo: r.c[0]?.v || "", 
            empresa: r.c[1]?.v || "",
            provincia: r.c[2]?.v || "", 
            link: r.c[3]?.v || "",
            fotoCapa: r.c[4]?.v || "" 
        }));

        renderListaVagas(todasAsVagas);
        renderCarrossel(listaServicos);
    } catch (erro) {
        console.error("Erro ao carregar dados. Verifique a planilha.");
    }
}

// 7. INICIALIZAÇÃO
window.onload = () => {
    carregarDados();
    rodarSlides();
    document.getElementById('inputBusca')?.addEventListener('input', filtrarVagas);
    document.getElementById('selectProvincia')?.addEventListener('change', filtrarVagas);
};

function abrirTermos() { document.getElementById("modalTermos").style.display = "block"; }
function fecharTermos() { document.getElementById("modalTermos").style.display = "none"; }
