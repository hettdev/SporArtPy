using Prism.Commands;
using Prism.Mvvm;
using Prism.Navigation;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;

namespace BrightnessController.App.ViewModels
{
    public class MainPageViewModel : ViewModelBase
    {
        private string _address;
        public string Address
        {
            get { return _address; }
            set { SetProperty(ref _address, value); }
        }

        private DelegateCommand _submitCommand;
        public DelegateCommand SubmitCommand
        {
            get { return _submitCommand; }
            set { SetProperty(ref _submitCommand, value); }
        }

        private bool _addressSubmitted = false;
        public bool AddressSubmitted
        {
            get { return _addressSubmitted; }
            set { SetProperty(ref _addressSubmitted, value); }
        }

        private double _sliderValue;
        public double SliderValue
        {
            get { return _sliderValue; }
            set { SetProperty(ref _sliderValue, value); }
        }

        private DelegateCommand _sliderValueChangedCommand;
        public DelegateCommand SliderValueChangedCommand
        {
            get { return _sliderValueChangedCommand; }
            set { SetProperty(ref _sliderValueChangedCommand, value); }
        }

        public MainPageViewModel(INavigationService navigationService)
            : base(navigationService)
        {
            Title = "Main Page";
            _submitCommand = new DelegateCommand(() => OnAdressSubmitted());
            _sliderValueChangedCommand = new DelegateCommand(() => OnSliderValueChanged());
        }

        private void OnSliderValueChanged()
        {
            Debug.WriteLine($"Slidervalue changed to {SliderValue}");
        }

        private void OnAdressSubmitted()
        {
            AddressSubmitted = true;
        }
    }
}
