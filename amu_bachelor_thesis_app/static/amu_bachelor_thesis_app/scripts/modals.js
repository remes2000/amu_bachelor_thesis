const app_name = 'amu_bachelor_thesis';

// STUDENT CONFIRM THESIS SELECT MODAL
document.querySelectorAll('.modal__student_confirm_thesis_select').forEach(b => {
    b.addEventListener('click', () => {
        const thesisId = b.dataset.thesisId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Wybieranie tematu pracy</p>
                    </header>
                    <section class="modal-card-body">
                        Czy na pewno chcesz wybrać ten temat pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis', thesisId, 'select']);
        showModal(template, successCallback)
    });
});

// STUDENT CONFIRM THESIS UNSELECT MODAL
document.querySelectorAll('.modal__student_confirm_thesis_unselect').forEach(b => {
    b.addEventListener('click', () => {
        const thesisId = b.dataset.thesisId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Porzucanie tematu pracy</p>
                    </header>
                    <section class="modal-card-body">
                        Czu na pewno chcesz porzucić ten temat pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis', thesisId, 'unselect']);
        showModal(template, successCallback)
    });
});

// LECTURER CONFIRM THESIS PROPOSITION
document.querySelectorAll('.modal__lecturer_confirm_thesis_proposition').forEach(b => {
    b.addEventListener('click', () => {
        const thesisPropositionId = b.dataset.thesisPropositionId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Akceptowanie propozycji tematu</p>
                    </header>
                    <section class="modal-card-body">
                        Czy na pewno chcesz zaakceptować tą propozycję tematu pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis_proposition', thesisPropositionId, 'accept']);
        showModal(template, successCallback);
    });
});

// LECTURER DISCARD THESIS PROPOSITION
document.querySelectorAll('.modal__lecturer_discard_thesis_proposition').forEach(b => {
    b.addEventListener('click', () => {
        const thesisPropositionId = b.dataset.thesisPropositionId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Odrzucanie propozycji tematu</p>
                    </header>
                    <section class="modal-card-body">
                        Czu na pewno chcesz odrzucić tą propozycję tematu pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis_proposition', thesisPropositionId, 'discard']);
        showModal(template, successCallback);
    });
});

//STUDENT DISCARD OWN THESIS PROPOSITION
document.querySelectorAll('.modal__student_discard_own_thesis_proposition').forEach(b => {
    b.addEventListener('click', () => {
        const thesisPropositionId = b.dataset.thesisPropositionId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Anulowanie propozycji tematu</p>
                    </header>
                    <section class="modal-card-body">
                        Czu na pewno chcesz anulować tą propozycję tematu pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis_proposition', thesisPropositionId, 'discard_own']);
        showModal(template, successCallback);
    });
});

//STUDENT RESEND THESIS PROPOSITION
document.querySelectorAll('.modal__student_resend_thesis_proposition').forEach(b => {
    b.addEventListener('click', () => {
        const thesisPropositionId = b.dataset.thesisPropositionId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Ponowne przesyłanie propozycji</p>
                    </header>
                    <section class="modal-card-body">
                        Czu na pewno chcesz ponownie przesłać tą propozycję tematu pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis_proposition', thesisPropositionId, 'resend']);
        showModal(template, successCallback);
    });
});

// LECTURER REMOVE THESIS
document.querySelectorAll('.modal__lecturer_remove_thesis').forEach(b => {
    b.addEventListener('click', () => {
        const thesisId = b.dataset.thesisId;
        const template =`
            <div class="modal is-active">
                <div class="modal-background close-modal"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Usuwanie tematu pracy</p>
                    </header>
                    <section class="modal-card-body">
                        Czu na pewno chcesz usunąć ten temat pracy inżynierskiej?
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success success">Tak</button>
                        <button class="button close-modal">Anuluj</button>
                    </footer>
                </div>
            </div>
        `;
        const successCallback = () => setLocation(['thesis', thesisId, 'remove']);
        showModal(template, successCallback);
    });
});

function showModal(template, successCallback) {
    const modalContainer = document.createElement('div');
    modalContainer.classList.add('active-modal');
    modalContainer.innerHTML = template;
    modalContainer.querySelectorAll('.close-modal').forEach(e => {
        e.addEventListener('click', () => {
            closeModal();
        });
    });
    modalContainer.querySelector('.success').addEventListener('click', () => {
        successCallback();
    });
    document.querySelector('body').appendChild(modalContainer);
}

function closeModal() {
    const body = document.querySelector('body');
    const modal = body.querySelector('.active-modal');
    if(modal) {
        body.removeChild(modal);
    }
}

function setLocation(urlParts) {
    window.location.href = ['/' + app_name].concat(urlParts).join('/');
}

document.addEventListener('keyup', (e) => {
    if(e.key === 'Escape') {
        closeModal();
    }
});