using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Runtime.InteropServices;
using System.Threading;

namespace IndoMarketInsightLauncher;

class Program
{
    static int Main(string[] args)
    {
        Console.Title = "IndoMarket Insight Launcher";
        Banner();
        try
        {
            string root = FindProjectRoot();
            Console.WriteLine($"Project folder: {root}");
            Directory.SetCurrentDirectory(root);

            string python = EnsurePythonAndVenv(root);
            Run(python, "-m pip install --upgrade pip", root, "Upgrading pip");
            Run(python, "-m pip install -r requirements.txt", root, "Installing/updating dependencies");
            Run(python, "app/init_db.py", root, "Initializing database");

            Console.WriteLine();
            Console.WriteLine("Starting IndoMarket Insight at http://localhost:8501 ...");
            var streamlit = StartProcess(python, "-m streamlit run app/main.py --server.headless true --server.port 8501", root, inheritConsole: true);

            WaitForUrl("http://localhost:8501", TimeSpan.FromSeconds(45));
            OpenBrowser("http://localhost:8501");

            Console.WriteLine();
            Console.WriteLine("IndoMarket Insight is running.");
            Console.WriteLine("Keep this window open. Close it to stop the app.");
            Console.WriteLine("Press Ctrl+C to stop.");
            streamlit.WaitForExit();
            return streamlit.ExitCode;
        }
        catch (Exception ex)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("Launcher failed:");
            Console.WriteLine(ex.Message);
            Console.ResetColor();
            Console.WriteLine();
            Console.WriteLine("Troubleshooting:");
            Console.WriteLine("1. Install Python 3.10+ from https://www.python.org/downloads/");
            Console.WriteLine("2. Make sure 'Add Python to PATH' is enabled.");
            Console.WriteLine("3. Run this EXE from inside the extracted indomarket_insight folder.");
            Console.WriteLine("4. If Windows blocks it, right-click > Properties > Unblock.");
            Console.WriteLine();
            Console.WriteLine("Press Enter to exit...");
            Console.ReadLine();
            return 1;
        }
    }

    static void Banner()
    {
        Console.ForegroundColor = ConsoleColor.Cyan;
        Console.WriteLine("===================================================");
        Console.WriteLine("       IndoMarket Insight - One Click Launcher      ");
        Console.WriteLine("===================================================");
        Console.ResetColor();
        Console.WriteLine("This launcher prepares Python, installs dependencies,");
        Console.WriteLine("starts Streamlit, and opens the dashboard.");
        Console.WriteLine();
    }

    static string FindProjectRoot()
    {
        string dir = AppContext.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        string? current = dir;
        for (int i = 0; i < 6 && current != null; i++)
        {
            if (File.Exists(Path.Combine(current, "app", "main.py")) && File.Exists(Path.Combine(current, "requirements.txt")))
                return current;
            current = Directory.GetParent(current)?.FullName;
        }
        string cwd = Directory.GetCurrentDirectory();
        if (File.Exists(Path.Combine(cwd, "app", "main.py")) && File.Exists(Path.Combine(cwd, "requirements.txt")))
            return cwd;
        throw new DirectoryNotFoundException("Could not find app/main.py and requirements.txt. Put IndoMarketInsight.exe in the indomarket_insight project folder.");
    }

    static string EnsurePythonAndVenv(string root)
    {
        string venvPython = Path.Combine(root, ".venv", "Scripts", "python.exe");
        if (File.Exists(venvPython))
        {
            Console.WriteLine("Using existing virtual environment.");
            return venvPython;
        }

        string pyLauncher = FindCommand("py", "-3 --version") ?? FindCommand("python", "--version") ?? FindCommand("python3", "--version")
            ?? throw new Exception("Python was not found. Install Python 3.10+ and enable 'Add Python to PATH'.");

        Console.WriteLine($"Creating virtual environment using: {pyLauncher}");
        if (Path.GetFileName(pyLauncher).Equals("py.exe", StringComparison.OrdinalIgnoreCase) || Path.GetFileName(pyLauncher).Equals("py", StringComparison.OrdinalIgnoreCase))
            Run(pyLauncher, "-3 -m venv .venv", root, "Creating .venv");
        else
            Run(pyLauncher, "-m venv .venv", root, "Creating .venv");

        if (!File.Exists(venvPython))
            throw new FileNotFoundException("Virtual environment creation failed; .venv/Scripts/python.exe was not created.");
        return venvPython;
    }

    static string? FindCommand(string command, string testArgs)
    {
        try
        {
            var p = StartProcess(command, testArgs, Directory.GetCurrentDirectory(), inheritConsole: false);
            if (p.WaitForExit(8000) && p.ExitCode == 0)
                return command;
        }
        catch { }
        return null;
    }

    static void Run(string fileName, string arguments, string workingDirectory, string label)
    {
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine($"\n[{label}]");
        Console.ResetColor();
        var p = StartProcess(fileName, arguments, workingDirectory, inheritConsole: true);
        p.WaitForExit();
        if (p.ExitCode != 0)
            throw new Exception($"Command failed during '{label}' with exit code {p.ExitCode}: {fileName} {arguments}");
    }

    static Process StartProcess(string fileName, string arguments, string workingDirectory, bool inheritConsole)
    {
        var psi = new ProcessStartInfo
        {
            FileName = fileName,
            Arguments = arguments,
            WorkingDirectory = workingDirectory,
            UseShellExecute = false,
            RedirectStandardOutput = !inheritConsole,
            RedirectStandardError = !inheritConsole,
            CreateNoWindow = false
        };
        var p = Process.Start(psi) ?? throw new Exception($"Could not start process: {fileName}");
        return p;
    }

    static void WaitForUrl(string url, TimeSpan timeout)
    {
        var deadline = DateTime.UtcNow + timeout;
        using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
        while (DateTime.UtcNow < deadline)
        {
            try
            {
                var response = client.GetAsync(url).Result;
                if ((int)response.StatusCode < 500) return;
            }
            catch { }
            Thread.Sleep(1000);
        }
    }

    static void OpenBrowser(string url)
    {
        try
        {
            Process.Start(new ProcessStartInfo { FileName = url, UseShellExecute = true });
        }
        catch
        {
            Console.WriteLine($"Open your browser manually: {url}");
        }
    }
}
