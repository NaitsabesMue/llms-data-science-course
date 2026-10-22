"""Week 4 final test: 20 hand-written synthetic requests, four per label.

Load only after development. These replace the old overlapping evaluation set.
They are teaching examples, not observations of real student traffic.
"""

eval_data = [
    {"text": "Le cours de statistiques a-t-il changé d'amphi ?", "label": "get_schedule"},
    {"text": "Est-ce que la séance de chimie a été annulée ?", "label": "get_schedule"},
    {"text": "Je change de groupe de TD, où voir mes nouveaux créneaux ?", "label": "get_schedule"},
    {"text": "À quelle date se termine notre dernière séance de physique ?", "label": "get_schedule"},
    {"text": "Comment retrouver un message dans les éléments envoyés ?", "label": "check_email"},
    {"text": "Le courrier de mon enseignant est peut-être dans les indésirables", "label": "check_email"},
    {"text": "Je voudrais ouvrir la pièce jointe reçue de la scolarité", "label": "check_email"},
    {"text": "Mon espace de stockage de courriels est plein", "label": "check_email"},
    {"text": "J'aimerais remplacer mon option de cinéma par une option de musique", "label": "register_classes"},
    {"text": "Une unité d'enseignement manque dans mon inscription pédagogique", "label": "register_classes"},
    {"text": "J'ai validé la mauvaise option, comment corriger mon choix ?", "label": "register_classes"},
    {"text": "Je veux abandonner une matière facultative ce semestre", "label": "register_classes"},
    {"text": "Le nom imprimé sur mon badge étudiant est erroné", "label": "get_student_card"},
    {"text": "Puis-je changer la photo de ma carte étudiante ?", "label": "get_student_card"},
    {"text": "J'ai retrouvé ma carte après l'avoir déclarée perdue", "label": "get_student_card"},
    {"text": "Le paiement du remplacement de ma carte a été refusé", "label": "get_student_card"},
    {"text": "Est-ce que la bibliothèque dispose d'une salle de travail en groupe ?", "label": "find_library_info"},
    {"text": "Je cherche une prise électrique dans les espaces de lecture de la BU", "label": "find_library_info"},
    {"text": "Une pénalité apparaît sur mon compte lecteur, qui contacter ?", "label": "find_library_info"},
    {"text": "Comment consulter les revues numériques de la bibliothèque depuis chez moi ?", "label": "find_library_info"},
]
