#ifndef QVAR_H
#define QVAR_H

#include <QMainWindow>

namespace Ui {
class QVAR;
}

class QVAR : public QMainWindow
{
    Q_OBJECT

public:
    explicit QVAR(QWidget *parent = nullptr);
    ~QVAR();

private:
    Ui::QVAR *ui;
};

#endif // QVAR_H
