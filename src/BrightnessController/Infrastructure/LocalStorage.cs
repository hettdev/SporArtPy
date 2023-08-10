using BrightnessController.Abstractions;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Serilog;

namespace BrightnessController.Infrastructure
{
    public class LocalStorage : ILocalStorage
    {
        private const string StorageFile = "brightnessStorage";
        private readonly ILogger _logger;

        public LocalStorage(ILogger logger)
        {
            _logger = logger;
        }

        public async Task<int> GetBrightness()
        {
            try
            {
                var res = File.ReadAllText(StorageFile);
                return Int32.Parse(res);
            }
            catch (Exception)
            {
                return 100;
            }
        }

        public async Task StoreBrightness(int brightness)
        {
            await File.WriteAllTextAsync(StorageFile, brightness.ToString());
            _logger.Information($"storing {brightness}");
        }
    }
}