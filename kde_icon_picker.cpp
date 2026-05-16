#include <KIconDialog>
#include <QApplication>
#include <QDebug>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    // Open the KDE icon picker dialog
    QString iconName = KIconDialog::getIcon(nullptr, QString(), QString(), QString());

    if (!iconName.isEmpty()) {
        // Print the selected icon name to stdout
        qDebug().noquote() << iconName;
        return 0;
    }

    return 1; // no icon selected
}
