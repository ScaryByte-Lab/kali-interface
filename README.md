# CyberListen Terminal v1.0 (For Kali Linux)

![CyberListen Terminal](https://github.com/ScaryByte-Lab/kali-interface/blob/main/97d29801-3a91-49f3-abd1-45a5a2ed4085.webp)

CyberListen Terminal is a web interface that allows you to run network commands and queries on a Kali terminal. The interface is designed to be user-friendly and professional, offering predefined commands, advanced queries, and custom command line inputs.

## Features

- Run custom command line inputs
- Execute predefined network commands
- Perform advanced network queries with target inputs
- User-friendly interface with dark theme
- Real-time command execution with progress indicators

## Installation

Follow these steps to set up the CyberListen Terminal on your local machine or Raspberry Pi with Kali Linux.

### Prerequisites

- Kali Linux installed on your system (Raspberry Pi or any other device)
- Python 3.x installed
- pip (Python package installer) installed

### Step-by-Step Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ScaryByte-Lab/kali-interface.git
    cd kali-interface
    ```

2. **Install Flask**

    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install Flask
    ```

3. **Create the Flask App**

    Ensure the following files exist in your repository:

    - `app.py`
    - `templates/index.html`

4. **Flask App (`app.py`)**

    ```python
    from flask import Flask, request, render_template, jsonify
    import subprocess

    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/run_command', methods=['POST'])
    def run_command():
        command = request.form.get('command')

        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return jsonify({'result': result})
        except subprocess.CalledProcessError as e:
            return jsonify({'result': e.output}), 400

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```

5. **HTML Template (`templates/index.html`)**

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CyberListen Terminal</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                min-height: 100vh;
            }
            .container {
                margin-top: 50px;
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .header, .footer {
                background-color: #1a1a1a;
                padding: 10px;
                text-align: center;
                width: 100%;
            }
            .box {
                border: 1px solid #444;
                padding: 20px;
                border-radius: 5px;
                background-color: #333;
                width: 100%;
                max-width: 800px;
            }
            .box .form-group label {
                color: #cccccc;
            }
            .form-control {
                background-color: #222;
                color: #fff;
                border: 1px solid #555;
            }
            .form-control:focus {
                background-color: #333;
                color: #fff;
                border-color: #777;
            }
            .btn-primary {
                background-color: #007bff;
                border: none;
            }
            .btn-primary:hover {
                background-color: #0056b3;
            }
            #output {
                background-color: #2d2d2d;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
                max-height: 400px;
                overflow-y: auto;
                overflow-x: auto;
                white-space: pre-wrap;
                font-family: 'Courier New', Courier, monospace;
                color: #e0e0e0;
            }
            .progress {
                height: 20px;
            }
            .alert {
                color: #ffffff;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CyberListen Terminal</h1>
        </div>
        <div class="container">
            <div class="box">
                <form id="commandForm">
                    <div class="form-group">
                        <label for="commandType">Choose Command Type:</label>
                        <select class="form-control" id="commandType" name="commandType" required>
                            <option value="">Select command type</option>
                            <option value="commandLine">Command Line</option>
                            <option value="predefinedCommand">Predefined Command</option>
                            <option value="advancedQuery">Advanced Query</option>
                        </select>
                    </div>
                    <div class="form-group" id="commandLineGroup" style="display:none;">
                        <label for="command">Enter Command:</label>
                        <input type="text" class="form-control" id="command" name="command" placeholder="e.g. nmap -sP 192.168.1.0/24">
                    </div>
                    <div class="form-group" id="predefinedCommandGroup" style="display:none;">
                        <label for="predefinedCommand">Select a predefined command:</label>
                        <select class="form-control" id="predefinedCommand" name="predefinedCommand">
                            <option value="">Select a command</option>
                            <option value="ifconfig">ifconfig</option>
                            <option value="netstat">netstat</option>
                            <option value="traceroute">traceroute</option>
                            <option value="ping -c 4 8.8.8.8">ping (Google DNS)</option>
                        </select>
                    </div>
                    <div class="form-group" id="advancedQueryGroup" style="display:none;">
                        <label for="advancedQuery">Select an advanced query:</label>
                        <select class="form-control" id="advancedQuery" name="advancedQuery">
                            <option value="">Select an advanced query</option>
                            <option value="nmap -vv -A -Pn -p-">Nmap Full Scan</option>
                            <option value="nikto -h">Nikto Scan</option>
                        </select>
                        <label for="target" class="mt-2">Enter Target:</label>
                        <input type="text" class="form-control" id="target" name="target" placeholder="e.g. 192.168.1.1">
                    </div>
                    <button type="submit" class="btn btn-primary">Run Command</button>
                </form>
                <div class="progress mt-3" id="progressBar" style="display: none;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 100%"></div>
                </div>
                <div id="output" class="mt-3"></div>
            </div>
        </div>
        <div class="footer">
            <p>&copy; 2024 CyberListen Terminal</p>
        </div>
        <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
        <script>
            $('#commandType').on('change', function() {
                var commandType = $(this).val();
                $('#commandLineGroup').hide();
                $('#predefinedCommandGroup').hide();
                $('#advancedQueryGroup').hide();
                if (commandType === 'commandLine') {
                    $('#commandLineGroup').show();
                } else if (commandType === 'predefinedCommand') {
                    $('#predefinedCommandGroup').show();
                } else if (commandType === 'advancedQuery') {
                    $('#advancedQueryGroup').show();
                }
            });

            $('#commandForm').on('submit', function(e) {
                e.preventDefault();
                var commandType = $('#commandType').val();
                var command = '';
                
                if (commandType === 'commandLine') {
                    command = $('#command').val();
                } else if (commandType === 'predefinedCommand') {
                    command = $('#predefinedCommand').val();
                } else if (commandType === 'advancedQuery') {
                    var advancedQuery = $('#advancedQuery').val();
                    var target = $('#target').val();
                    if (!target) {
                        $('#output').html('<div class="alert alert-danger" role="alert">Please enter a target for the advanced query.</div>');
                        return;
                    }
                    command = advancedQuery + ' ' + target;
                }

                if (!command) {
                    $('#output').html('<div class="alert alert-danger" role="alert">Please enter or select a command.</div>');
                    return;
                }

                $('#output').html('');
                $('#progressBar').show();

                $.ajax({
                    url: '/run_command',
                    type: 'POST',
                    data: { command: command },
                    success: function(response) {
                        $('#progressBar').hide();
                        $('#output').html('<pre>' + response.result + '</pre>');
                    },
                    error: function(response) {
                        $('#progressBar').hide();
                        $('#output').html('<div class="alert alert-danger" role="alert">Error: ' + response.responseJSON.result + '</div>');
                    }
                });
            });
        </script>
    </body>
    </html>
    ```

### Usage

1. **Start the Flask Application**

    ```bash
    python3 app.py
    ```

2. **Access the Web Interface**

    Open a web browser and navigate to `http://<your_raspberry_pi_ip>:5000`.

3. **Choose Command Type**

    - **Command Line**: Enter a custom command.
    - **Predefined Command**: Select a predefined command from the dropdown.
    - **Advanced Query**: Select an advanced query and enter the target.

4. **Run Command**

    Click the "Run Command" button to execute the selected command. The output will be displayed in the terminal section.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

Enjoy using CyberListen Terminal! If you encounter any issues, please open an issue on GitHub.
