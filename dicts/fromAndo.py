# SSID when resetting the WiFi
SSID_reset = "__RAS__"

listOfLanguages = [
  "ENGLISH",
  "ESPAÑOL",
  "FRANÇAIS"
]

# allows to display the different messages by defining the parameters needed to  use
# the function multiline of luma.core
#
# [ (x0,y0), font size , text of the message]
#
# (x0,y0) positions the message in the screen defining the origin
# the message can extend over several lines this is indicated with the escape character \n

messages_dic = {
    ' ':
        {
          "ENGLISH": [(0, 0), 20,' '],
          "ESPAÑOL": [(0, 0), 20,' '],
          "FRANÇAIS": [(0, 0), 20,' ']
        },

    'welcome':
        {
          "ENGLISH": [(5, 10), 15, 'Welcome to the' + '\n' +'RFID attendance' + '\n' + 'system'],
          "ESPAÑOL": [(0, 0), 14, 'Sistema de' + '\n' +'Control' + '\n' +'de Presencia' + '\n' + 'por RFID' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 0), 14, 'Bienvenue sur' + '\n' +'sur votre badgeuse' + '\n' +'connectée à EtRH']
        },

    'wait':
        {
          "ENGLISH": [(0, 6), 18, 'Please' + '\n' +'wait' + '\n' + '\n' + "-"*14],
          "ESPAÑOL": [(0, 6), 18, 'Espere' + '\n' +'por favor' + '\n' + '\n' + "-"*14],
          "FRANÇAIS": [(0, 6), 18, 'Veuillez' + '\n' +'patienter' + '\n' + '\n' + "-"*14]
        },

    'check_in':
        {
          "ENGLISH": [(0, 6), 16,'>>> CHECK IN ...' + '\n' + '-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14],
          "ESPAÑOL": [(0, 6), 16,'>>> Entrada .....' + '\n' +'-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14],
          "FRANÇAIS": [(0, 6), 16,'>>> BIENVENUE .....' + '\n' +'-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14]
        },


    'check_out':
        {
          "ENGLISH": [(0, 6), 16,'CHECK OUT >>>' + '\n' + '-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14],
          "ESPAÑOL": [(0, 6), 16,'...... Salida >>>>' + '\n' + '-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14],
          "FRANÇAIS": [(0, 6), 16,'AU REVOIR >>>>' + '\n' + '-EmployeePlaceholder-' + '\n' + '\n' + '\n' + "-"*14]
        },

    'FALSE':
        {
          "ENGLISH": [(0, 12), 16,'NOT' + '\n' +'AUTHORIZED' + '\n' + '\n' + "-"*16],
          "ESPAÑOL": [(0, 12), 16,' NO' + '\n' +'AUTORIZADO' + '\n' + '\n' + "-"*16],
          "FRANÇAIS": [(0, 12), 16,' BADGE' + '\n' +'NON RECONNU' + '\n' + '\n' + "-"*16]
        },


    'ContactAdm':
        {
          "ENGLISH": [(0, 6), 15, 'Contact' + '\n' +'your' + '\n' +'Administrator' + '\n' + '\n' + "-"*18],
          "ESPAÑOL": [(0, 6), 15,'Contacte' + '\n' +'con su' + '\n' +'Informático' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 6), 15,'Contactez votre' + '\n' +' Responsable' + '\n' +'Informatique' + '\n' + '\n' + "-"*18]
        },

    'connecting':
        {
          "ENGLISH": [(1, 2), 18,' ' + '\n' + '.. connecting...' + '\n' + '\n' + '\n' + "-"*15],
          "ESPAÑOL": [(1, 2), 18,' ' + '\n' + '.. conectando...' + '\n' + '\n' + '\n' + "-"*15],
          "FRANÇAIS": [(1, 2), 18,' ' + '\n' + '.. connexion...' + '\n' + '\n' + '\n' + "-"*15]
        },

    'yes':
        {
          "ENGLISH": [(1, 2), 18,' ' + '\n' + 'YES' + '\n' + '\n' + '\n' + "-"*15],
          "ESPAÑOL": [(1, 2), 18,' ' + '\n' + 'SI' + '\n' + '\n' + '\n' + "-"*15],
          "FRANÇAIS": [(1, 2), 18,' ' + '\n' + 'OUI' + '\n' + '\n' + '\n' + "-"*15]
        },

    'no':
        {
          "ENGLISH": [(1, 2), 18,' ' + '\n' + 'NO' + '\n' + '\n' + '\n' + "-"*15],
          "ESPAÑOL": [(1, 2), 18,' ' + '\n' + 'NO' + '\n' + '\n' + '\n' + "-"*15],
          "FRANÇAIS": [(1, 2), 18,' ' + '\n' + 'NON' + '\n' + '\n' + '\n' + "-"*15]
        },



    'comm_failed':
        {
          "ENGLISH": [(0, 6), 15,'Error while' + '\n' + 'communicating' + '\n' + 'with EtRH' + '\n' + '\n' + "-"*18],
          "ESPAÑOL": [(0, 6), 15,'Error mientras' + '\n' + 'comunicando' + '\n' + 'con EtRH' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 6), 15,'Echec de' + '\n' + 'la connexion' + '\n' + 'avec EtRH' + '\n' + '\n' + "-"*18]
        },

    'EtRH_failed':
        {
          "ENGLISH": [(0, 0), 14,'Communication' + '\n' + 'with EtRH FAILED,' + '\n' + 'please check' + '\n' + 'the parameters' + '\n' + "-"*18],
          "ESPAÑOL": [(0, 0), 14,'La comunicación' + '\n' + 'con EtRH ha fallado' + '\n' + 'Por favor, revise' + '\n' + 'los parámetros' + '\n' + "-"*17],
          "FRANÇAIS": [(0, 0), 14,'Echec de la connexion' + '\n' + 'avec le serveur EtRH' + '\n' + 'Veuillez, vérifier' + '\n' + 'vos paramètres' + '\n' + "-"*17]
        },

    'no_wifi':
        {
          "ENGLISH": [(0, 4), 18, 'No' + '\n' +'WiFi' + '\n' +'Signal' + '\n' + '\n' + "-"*14],
          "ESPAÑOL": [(0, 4), 18, 'No hay' + '\n' +'Señal' + '\n' +'WiFi' + '\n' + '\n' + "-"*14],
          "FRANÇAIS": [(0, 4), 18, 'Aucun' + '\n' +'Signal WIFI' + '\n' +'détecté' + '\n' + '\n' + "-"*14],
        },

    'gotEtRHUID':
        {
          "ENGLISH": [(0, 6), 15,'Communication' + '\n' +'with EtRH' + '\n' +'established' + '\n' + '\n' + "-"*18],
          "ESPAÑOL": [(0, 6), 15,'Communicación' + '\n' +'con EtRH' + '\n' +'establecida' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 6), 15,'Connexion établie' + '\n' +'avec votre' + '\n' +'serveur EtRH' + '\n' + '\n' + "-"*18],
        },

    'noEtRHUID':
        {
          "ENGLISH": [(0,6), 16, "Could not get" + '\n' +'an EtRH' + '\n' +'UID' '\n' + "-"*16],
          "ESPAÑOL": [(0,6), 15,'No fué posible' + '\n' +'conseguir una' + '\n' +'UID en EtRH' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0,6), 15,'No fué posible' + '\n' +'conseguir una' + '\n' +'UID en EtRH' + '\n' + '\n' + "-"*18],
        },

    'configure_wifi':
      {
        "ENGLISH": [(0, 0), 14, '1. Connect to AP' + '\n' + SSID_reset + '\n' + '2. Browse to ' + '\n' + '192.168.42.1' + '\n' + "-"*18 + '\n' ],
        "ESPAÑOL": [(0, 0), 14, '1. Conéctese al AP' + '\n' + SSID_reset + '\n' + '2. Navege a ' + '\n' + '192.168.42.1' + '\n' + "-"*18 + '\n' ],
        "FRANÇAIS": [(0, 0), 14, '1. Connectez-vous au SSID' + '\n' + SSID_reset + '\n' + '2. Ouvrez l\'URL ' + '\n' + '192.168.42.1' + '\n' + "-"*18 + '\n' ],
      },

    'rebooting':
      {
        "ENGLISH": [(0, 0), 16, '\n' + 'REBOOTING' + '\n' + '\n' + '\n' + "-"*16],
        "ESPAÑOL": [(0, 6), 16, 'Reinicializando' + '\n' + 'el terminal' + '\n' + '-rebooting-' + '\n' + '\n' + "-"*16],
        "FRANÇAIS": [(0, 6), 16, 'REDÉMARRAGE' + '\n' + '\n' + '\n' + "-"*16],
      },

    'shuttingDown':
      {
        "ENGLISH": [(0, 12), 16, 'SHUTTING' + '\n' +'DOWN' + '\n' + '\n' + '\n' + "-"*16],
        "ESPAÑOL": [(0, 0), 16, 'Apagando' + '\n' + 'el terminal' + '\n' + '-shutting down-' + '\n' + '\n' + "-"*16],
        "FRANÇAIS": [(0, 0), 16, 'ARRÊT' + '\n' +'EN COURS' + '\n' + '\n' + '\n' + "-"*16],
      },

    'ERRUpdate':
      {
        "ENGLISH": [(0, 6), 14,'Unable to update,' + '\n' + 'GitHub is not' + '\n' +'available' + '\n' + '\n' +'-'*18],
        "ESPAÑOL": [(0, 6), 14,'Update no es' + '\n' + 'posible, GitHub' + '\n' +'no responde' + '\n' + '\n' +'-'*18],
        "FRANÇAIS": [(0, 6), 14,'Mise à jour impossible' + '\n' + 'GitHub' + '\n' +'ne répond pas' + '\n' + '\n' +'-'*18],
      },


    'update':
        {
          "ENGLISH": [(0, 10), 15,'Updating' + '\n' + 'the' + '\n' + 'Firmware' + '\n' + '\n' + "-"*18],
          "ESPAÑOL": [(0, 6), 15,'Actualizando' + '\n' + 'el' + '\n' + 'Firmware' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 6), 15,'Mise à jour' + '\n' + 'du Firmware' + '\n' + 'en cours' + '\n' + '\n' + "-"*18],
        },

    'swipecard':
        {
          "ENGLISH": [(0, 6), 16,'Please' + '\n' + 'swipe' + '\n' + 'your card' + '\n' + '\n' + "-"*16],
          "ESPAÑOL": [(0, 6), 16,'Por favor' + '\n' + 'pase una' + '\n' + 'tarjeta' + '\n' + '\n' + "-"*16],
          "FRANÇAIS": [(0, 6), 16,'Veuillez' + '\n' + 'présenter' + '\n' + 'votre badge' + '\n' + '\n' + "-"*16],
        },

    'clocking':
      {
        "ENGLISH": [(0, 6), 15,'press OK' + '\n' + 'to begin' + '\n' + 'CLOCKING' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK\npara empezar\na fichar' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour' + '\n' + 'commencer' + '\n' + '\n' + "-"*18]
      },

    'chooseLanguage':
      {
        "ENGLISH": [(0, 6), 15,'press OK' + '\n' + 'to change' + '\n' + 'LANGUAGE' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK' + '\n' + 'para cambiar' + '\n' + 'el IDIOMA' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour changer' + '\n' + ' la LANGUE' + '\n' + '\n' + "-"*18]
      },

    'showRFID':
      {
        "ENGLISH": [(0, 6), 15,'press OK' + '\n' + 'to read' + '\n' + 'RFID codes' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK para' + '\n' + 'leer los' + '\n' + 'códigos RFID' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour lire' + '\n' + 'le code RFID' + '\n' + '\n' + "-"*18]
      },

    'updateFirmware':
      {
        "ENGLISH": [(0, 6), 15,'press OK' + '\n' + 'to UPDATE' + '\n' + 'the Firmware' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK para' + '\n' + 'actualizar' + '\n' + 'el Firmware' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour mettre à jour' + '\n' + 'le Firmware' + '\n' + '\n' + "-"*18]
      },

    'shouldEmployeeNameBeDisplayed':
      {
        "ENGLISH": [(0, 0), 14,'press OK to' + '\n' + 'choose if the' + '\n' + 'employee name' + '\n' +'should be shown' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 0), 14,'pulse OK para' + '\n' + 'determinar si se' + '\n' + 'muestra el nombre' + '\n' +'del empleado''\n' + "-"*18],
        "FRANÇAIS": [(0, 0), 14,'appuyez sur OK' + '\n' + 'pour l\'option :' + '\n' + 'Afficher le nom' + '\n' +'de l\'employé' + '\n' + "-"*18]
      },

    'resetWifi':
      {
        "ENGLISH": [(0, 6), 15,'press OK to' + '\n' + 'RESET the WiFi' + '\n' + 'parameters' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK para' + '\n' + 'resetear la' + '\n' + 'conexión WiFi' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour réinitialiser' + '\n' + 'les paramètres WIFI' + '\n' + '\n' + "-"*18]
      },

    'resetEtRH':
      {
        "ENGLISH": [(0, 6), 15,'press OK to' + '\n' + 'RESET the EtRH' + '\n' + 'parameters' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 0), 14,'pulse OK para' + '\n' + 'resetear los' + '\n' + 'parámetros' + '\n' + 'de EtRH' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 0), 14,'appuyez sur OK' + '\n' + 'pour réinitialiser' + '\n' + 'les paramètres EtRH' + '\n' + '\n' + "-"*18]
      },

    'getNewAdminCard':
      {
        "ENGLISH": [(0, 6), 15,'press OK to' + '\n' + 'change the' + '\n' + 'ADMIN CARD' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 6), 15,'pulse OK para' + '\n' + 'cambiar la' + '\n' + 'tarjeta ADMIN' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour changer le' + '\n' + 'badge ADMIN' + '\n' + '\n' + "-"*18]
      },

    'showVersion':
      {
        "ENGLISH": [(0, 6), 15,'press OK to see' + '\n' + 'the Firmware' + '\n' + 'VERSION' + '\n' + '\n' + "-"*18 ],
        "ESPAÑOL": [(0, 6), 15,'pulse OK para' + '\n' + 'ver la VERSION\' + '\n' + 'del Firmware' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 6), 15,'appuyez sur OK' + '\n' + 'pour afficher la ' + '\n' + 'version du Firmware' + '\n' + '\n' + "-"*18]
      },

    'shutdownSafe':
      {
        "ENGLISH": [(0, 6), 15,'press OK to' + '\n' + 'safe' + '\n' + 'HUTDOWN\n' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 0), 14,'pulse OK para' + '\n' + '-- APAGAR --' + '\n' + 'el terminal' + '\n' + '-shutdown-' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 0), 14,'appuyez sur OK' + '\n' + 'pour éteindre la' + '\n' + 'badgeuse en sécurité' + '\n' + '\n' + "-"*18]
      },

    'reboot':
      {
        "ENGLISH": [(0, 6), 15,'press OK' + '\n' + 'to' + '\n' + 'REBOOT\n' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 3), 14,'pulse OK para' + '\n' + '-- REINICIAR --' + '\n' + 'el terminal\n-reboot-' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 3), 14,'appuyez sur OK' + '\n' + 'pour' + '\n' + 'REDÉMARRER' + '\n' + '\n' + "-"*18]
      },

    'sure?':
      {
        "ENGLISH": [(0, 6), 15,'ARE YOU SURE?' + '\n' + 'Press OK again' + '\n' + 'if you are sure' + '\n' + '\n' + "-"*18],
        "ESPAÑOL": [(0, 0), 14,'ESTÁ SEGURO?' + '\n' + 'Pulse OK otra' + '\n' + 'vez si' + '\n' + 'stá seguro' + '\n' + '\n' + "-"*18],
        "FRANÇAIS": [(0, 0), 14,'ÊTES-VOUS SÛR ?' + '\n' + 'Appuyez sur OK' + '\n' + 'pour confirmer' + '\n' + '\n' + "-"*18]
      },

    'newAdmCardDefined':
        {
          "ENGLISH": [(0, 6), 16,'New Admin' + '\n' + 'RFID Card' + '\n' + 'defined' + '\n' + '\n' + "-"*16],
          "ESPAÑOL": [(0, 3), 15,'Nueva Tarjeta' + '\n' + 'Admin' + '\n' + 'registrada' + '\n' + '\n' + "-"*18],
          "FRANÇAIS": [(0, 3), 15,'Votre nouveau' + '\n' + 'badge ADMIN est' + '\n' + 'pris en compte' + '\n' + '\n' + "-"*18]
        },

    'browseForNewAdminCard':
        {
          "ENGLISH": [(0, 0), 14,'Browse to' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'to introduce new' + '\n' + 'Admin Card RFID' + '\n' +'-'*18 + '\n'],
          "ESPAÑOL": [(0, 0), 14,'Navege a' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'para definir otra' + '\n' + 'tarjeta Admin' + '\n' +'-'*18 + '\n'],
          "FRANÇAIS": [(0, 0), 14,'Ouvrez l\'URL' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'pour un nouveau' + '\n' + 'badge ADMIN' + '\n' + '-'*18 + '\n']
        },

    'browseForNewEtRHParams':
        {
          "ENGLISH": [(0, 0), 14,'Browse to' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'to introduce new' + '\n' + 'EtRH parameters' + '\n' + '-'*18 + '\n'],
          "ESPAÑOL": [(0, 0), 14,'Navege a' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'para definir nuevos' + '\n' + 'Parámetros EtRH' + '\n' +'-'*18 + '\n'],
          "FRANÇAIS": [(0, 0), 14,'Ouvrez l\'URL' + '\n' + '-IpPlaceholder-' + ':3000' + '\n' + 'pour definir les' + '\n' + 'paramètres EtRH' + '\n' +'-'*18 + '\n']
        },
}
