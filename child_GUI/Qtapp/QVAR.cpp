#include "QVAR.h"
#include "ui_QVAR.h"

QVAR::QVAR(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::QVAR)
{
    ui->setupUi(this);
}

QVAR::~QVAR()
{
    delete ui;
}
