using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BrightnessController.Abstractions
{
    public interface ILocalStorage
    {
        public Task StoreBrightness(int brightness);

        public Task<int> GetBrightness();
    }
}
