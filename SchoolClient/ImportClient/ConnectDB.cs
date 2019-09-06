using ImportClient.Db;
using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ImportClient
{
    public partial class FrmConnectDB : Form
    {
        public FrmConnectDB()
        {
            InitializeComponent();
        }

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            if (keyData == Keys.Escape)
            {
                this.Close();
                return true;
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }

        private void BtnConnect_Click(object sender, EventArgs e)
        {
            try
            {
                DbInfo.server = txtServer.Text;
                DbInfo.port = int.Parse(txtPort.Text);
                DbInfo.uid = txtUID.Text;
                DbInfo.password = txtPassword.Text;
                DbInfo.database = txtDatabase.Text;
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string connectionString = 
                $"Server={DbInfo.server};" +
                $"Port={DbInfo.port};" +
                $"Database={DbInfo.database};" +
                $"Uid={DbInfo.uid};" +
                $"Pwd={DbInfo.password};";
            //MessageBox.Show(connectionString, "ConnectionString", MessageBoxButtons.OK);
            Console.WriteLine(connectionString);

            DbInfo.connection = new MySqlConnection(connectionString);
            try
            {
                DbInfo.connection.Open();
                MessageBox.Show("Connected Successfully!");
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
