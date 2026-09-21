from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


class McpConfig:
    @staticmethod
    def get_mysql_workbench():
        mysql_server_params = StdioServerParams(
            command=r"D:\python 12\Scripts\uv.exe",
            args=[
                "run",
                "--with",
                "mysql-mcp-server",
                "mysql_mcp_server"
            ],
            env={
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "root",
                "MYSQL_PASSWORD": "password",
                "MYSQL_DATABASE": "mydb"
            },
            read_timeout_seconds=60
        )

        return McpWorkbench(mysql_server_params)

    @staticmethod
    def get_rest_api_workbench():
        rest_api_server_params = StdioServerParams(
            command= "node",
        args= [
            "C:/Users/shali/AppData/Roaming/npm/node_modules/dkmaker-mcp-rest-api/build/index.js"
        ],
        env= {
            "REST_BASE_URL": "https://rahulshettyacademy.com",
            "HEADER_Accept": "application/json"
        }
        )
        return McpWorkbench(rest_api_server_params)

    @staticmethod
    def get_excel_workbench():

        excel_server_params = StdioServerParams(
            command= "cmd",
        args= [
            "/c",
            "npx",
            "--yes",
            "@negokaz/excel-mcp-server"
        ],
        env= {
            "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
        }
        )
        return McpWorkbench(server_params=excel_server_params)

    @staticmethod
    def get_filesystem_workbench():

        filesystem_server_params = StdioServerParams(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "D:\\files_claude"],
            read_timeout_seconds=60
        )
        return McpWorkbench(server_params=filesystem_server_params)