function push_notif(head, txt, bootstrap){
    $.NotificationApp.send(head, txt, "top-right", "rgba(0,0,0,0.2)", bootstrap)
}