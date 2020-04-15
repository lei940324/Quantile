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

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

private:
    Ui::QVAR *ui;
};

#endif // QVAR_H
