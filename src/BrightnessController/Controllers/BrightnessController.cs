using BrightnessController.Abstractions;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;

namespace BrightnessController
{
    [Route("api/brightness")]
    public class BrightnessController : ControllerBase
    {
        private readonly ILocalStorage _localStorage;
        public BrightnessController(ILocalStorage localStorage)
        {
            _localStorage = localStorage;
        }

        [HttpGet]
        public async Task<ActionResult<int>> Get()
        {
            var res = await _localStorage.GetBrightness();
            return Ok(res);
        }

        [HttpPost]
        public async Task<ActionResult> Set([FromBody] int brightness)
        {
            await _localStorage.StoreBrightness(brightness);
            return Ok();
        }
    }

}