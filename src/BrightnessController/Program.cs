using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BrightnessController.Abstractions;
using BrightnessController.Infrastructure;
using DryIoc;
using DryIoc.Microsoft.DependencyInjection;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace BrightnessController
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            var container = new Container();
            container.Register<ILocalStorage, LocalStorage>();

            var host = new HostBuilder()
                .ConfigureWebHostDefaults((builder) =>
                {
                    builder.UseStartup<Startup>();
                })
                .UseServiceProviderFactory(new DryIocServiceProviderFactory(container))
                .Build();

            await host.RunAsync();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.UseStartup<Startup>();
                });
    }
}
