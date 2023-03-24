using BrightnessController.Abstractions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System;
using System.Threading.Tasks;

namespace BrightnessController
{
    [Route("api/brightness")]
    public class BrightnessController : ControllerBase
    {
        private readonly ILocalStorage _localStorage;
        private readonly string _authToken;

        public BrightnessController(ILocalStorage localStorage, IConfiguration config)
        {
            _localStorage = localStorage;
            _authToken = config["AuthToken"] ?? "";
        }

        [HttpGet]
        public async Task<ActionResult<int>> Get()
        {
            if (!IsAuthorized())
            {
                Console.WriteLine($"provided auth token {Request.Headers.Authorization} did not match expected token");
                return Unauthorized();
            }
            try
            {
                var res = await _localStorage.GetBrightness();
                return Ok(res);
            }
            catch (Exception ex)
            {
                return Problem(ex.Message);
            }
        }

        [HttpPost]
        public async Task<ActionResult> Set([FromBody] int brightness)
        {
            if (!IsAuthorized())
            {
                Console.WriteLine($"provided auth token {Request.Headers.Authorization} did not match expected token");
                return Unauthorized();
            }
            try
            {
                await _localStorage.StoreBrightness(brightness);
                return Ok();
            }
            catch (Exception ex)
            {
                return Problem(ex.Message);
            }
        }

        private bool IsAuthorized()
        {
            return !string.IsNullOrEmpty(_authToken)
                && Request.Headers.Authorization == _authToken;
        }
    }

}