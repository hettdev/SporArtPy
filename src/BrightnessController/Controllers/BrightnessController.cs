using BrightnessController.Abstractions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using System;
using System.Threading.Tasks;
using BrightnessController.Models;
using ImTools;
using Microsoft.Extensions.Hosting;
using Serilog;

namespace BrightnessController
{
    [Route("api/brightness")]
    public class BrightnessController : ControllerBase
    {
        private readonly ILocalStorage _localStorage;
        private readonly string _authToken;
        private readonly ILogger _logger;
        private readonly IHostEnvironment _environment;

        public BrightnessController(ILocalStorage localStorage, IConfiguration config, ILogger logger, IHostEnvironment environment)
        {
            _localStorage = localStorage;
            _logger = logger;
            _environment = environment;
            _authToken = config["AuthToken"] ?? "";
        }

        [HttpGet]
        public async Task<ActionResult<int>> Get()
        {
            if (!IsAuthorized())
            {
                _logger.Information($"provided auth token {Request.Headers.Authorization} did not match expected token");
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
        public async Task<ActionResult> Set([FromBody] double brightness)
        {
            try
            {
                var intValue = (int)brightness;
                _logger.Information($"Brightness POST: {intValue.ToString()}");
                if (!IsAuthorized())
                {
                    _logger.Information($"provided auth token {Request.Headers.Authorization} did not match expected token");
                    return Unauthorized();
                }
                await _localStorage.StoreBrightness(intValue);
                return Ok();
            }
            catch (Exception ex)
            {
                return Problem(ex.Message);
            }
        }

        private bool IsAuthorized()
        {
            return
                _environment.IsDevelopment()
                || (!string.IsNullOrEmpty(_authToken)
                    && Request.Headers.Authorization == _authToken);
        }
    }

}