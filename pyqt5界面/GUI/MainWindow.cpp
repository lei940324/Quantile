#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_action_triggered()
{

}

void MainWindow::on_action_2_triggered()
{

}

void MainWindow::on_action_3_triggered()
{

}

void MainWindow::on_action_4_triggered()
{

}

void MainWindow::on_doubleSpinBox_valueChanged(double arg1)
{

}

void MainWindow::on_pushButton_clicked()
{

}

void MainWindow::on_action_5_triggered()
{

}

void MainWindow::on_action_6_triggered()
{

}

void MainWindow::on_actionQVAR_triggered()
{

}
