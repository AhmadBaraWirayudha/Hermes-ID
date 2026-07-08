using System;
using System.Globalization;
using System.IO;
using System.Linq;

// Minimal CSV formatter for Indonesian market exports.
// Usage: dotnet run input.csv output.csv
class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 2)
        {
            Console.WriteLine("Usage: CsvFormatter <input.csv> <output.csv>");
            return;
        }
        var input = args[0];
        var output = args[1];
        var culture = new CultureInfo("id-ID");
        var lines = File.ReadAllLines(input);
        if (lines.Length == 0) return;
        var headers = lines[0].Split(',');
        int priceIdx = Array.FindIndex(headers, h => h.Trim().Equals("price", StringComparison.OrdinalIgnoreCase) || h.Trim().Equals("forecast_price", StringComparison.OrdinalIgnoreCase));
        using var writer = new StreamWriter(output);
        writer.WriteLine(lines[0] + ",price_idr_formatted");
        foreach (var line in lines.Skip(1))
        {
            var cells = line.Split(',');
            string formatted = "";
            if (priceIdx >= 0 && priceIdx < cells.Length && decimal.TryParse(cells[priceIdx], NumberStyles.Any, CultureInfo.InvariantCulture, out var value))
            {
                formatted = string.Format(culture, "Rp{0:N0}", value);
            }
            writer.WriteLine(line + "," + formatted);
        }
        Console.WriteLine($"Formatted CSV saved to {output}");
    }
}
