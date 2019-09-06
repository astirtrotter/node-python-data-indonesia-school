using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ImportClient.Db
{
    public static class DbInfo
    {
        public static string server { get; set; }
        public static int port { get; set; }
        public static string uid { get; set; }
        public static string password { get; set; }
        public static string database { get; set; }

        public static MySqlConnection connection { get; set; }
    }
}
